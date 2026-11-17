# LAB-04 — Báo cáo Mass Assignment

> Thực hiện: Viễn. Nhánh `lab/mass-assignment`.
> Chỉ kiểm thử trên crAPI local do nhóm tự triển khai.

## 1. Mục tiêu và phạm vi

- **OWASP API Security category:** API3:2023 — Broken Object Property Level Authorization
  (Mass Assignment); tương ứng API6:2019 — Mass Assignment.
- **crAPI challenge:** #8 — Get an item for free through an invalid refund workflow.
- **Tác động cần kiểm chứng:** client gửi các thuộc tính do server quản lý (`quantity`,
  `status`) để tăng số dư credit mà không thực sự mua/hoàn hàng.

## 2. Lý thuyết

- **Khái niệm:** Mass Assignment xảy ra khi API tự động gán các thuộc tính từ dữ liệu
  client gửi vào object nội bộ mà không giới hạn danh sách thuộc tính được phép. Client
  có thể ghi đè trường chỉ server/nghiệp vụ mới được đặt như `status`, `role`,
  `balance`, `quantity`.
- **Nguyên nhân thường gặp:**
  - Deserialize toàn bộ body vào model/serializer rồi `save()`.
  - Dùng chung serializer cho request và response, hoặc cho nhiều endpoint có quyền hạn
    khác nhau.
  - Thiếu validation nghiệp vụ (giá trị âm, trạng thái không hợp lệ theo luồng).
  - Endpoint "shadow"/không tài liệu vẫn tồn tại và chấp nhận trường ngoài schema.
- **Biện pháp phòng chống:** allowlist field rõ ràng; tách DTO cho từng thao tác; không
  nhận trường server-owned từ client; validate miền giá trị và luồng trạng thái; tính
  tiền/hoàn tiền phía server từ dữ liệu bất biến; kiểm tra quyền ở cấp thuộc tính.

## 3. Môi trường thực nghiệm

- **crAPI:** phiên bản `1.1.5`, commit `700f03d12a392d9e408260b4beae72ed02a4a1a4`
  (OWASP/crAPI, chạy bằng `bash scripts/crapi.sh up`).
- **Công cụ:** Docker Engine 29.9.2, Docker Compose 5.6.1, Python 3.14.8, pytest 9.2.0,
  httpx 0.28.1, python-dotenv 1.2.4.
- **Điều kiện ban đầu:** một tài khoản thử do test tự đăng ký, credit khởi tạo `$100`.
  Không ghi credentials/token thật vào repo.

## 4. Khảo sát chức năng bình thường

- **Mục đích nghiệp vụ:** người dùng mua sản phẩm trong Shop; mỗi đơn bị trừ
  `price × quantity`. Muốn hoàn hàng, người dùng tạo QR tại `return_order`, mang hàng đến
  UPS; trạng thái đơn do quy trình cửa hàng cập nhật, sau đó mới được hoàn tiền.
- **Endpoint liên quan:**
  - `GET /workshop/api/shop/products` — danh sách sản phẩm và credit hiện tại.
  - `POST /workshop/api/shop/orders` — tạo đơn, body `{"product_id":1,"quantity":1}`.
  - `POST /workshop/api/shop/orders/return_order?order_id=...` — tạo QR, đơn chuyển
    `return pending`.
  - `PUT /workshop/api/shop/orders/{order_id}` — cập nhật đơn (shadow API, không có trên
    UI; OpenAPI chỉ khai báo `product_id`, `quantity`).
- **Request/response hợp lệ:** xem [evidence/01-normal-flow.md](evidence/01-normal-flow.md).
  Credit `100 → 90` sau khi mua 1 sản phẩm $10.

## 5. Phương pháp kiểm thử

1. **Khởi tạo dữ liệu:** đăng ký tài khoản mới với email/số điện thoại ngẫu nhiên
   (`tests/security/test_mass_assignment.py::_signup_and_login`), đăng nhập lấy JWT.
2. **Kiểm thử có kiểm soát:**
   - Vector A: `POST /workshop/api/shop/orders` với `quantity=-5`.
   - Vector B: tạo đơn `quantity=1`, sau đó
     `PUT /workshop/api/shop/orders/{id}` với `{"product_id":1,"quantity":100,"status":"returned"}`.
   - Sau mỗi request, đọc lại credit từ `GET /workshop/api/shop/products`.
3. **Dấu hiệu xác nhận:** HTTP `200` thay vì `400/403`; credit tăng; response trả về
   `quantity`/`status` do client gửi.
4. **Cách chạy lại:**
   ```bash
   bash scripts/crapi.sh up
   source .venv/bin/activate
   pytest tests/security/test_mass_assignment.py -v
   ```

## 6. Bằng chứng

Đã làm sạch JWT, email và số điện thoại:

- [evidence/01-normal-flow.md](evidence/01-normal-flow.md) — luồng hợp lệ.
- [evidence/02-negative-quantity.md](evidence/02-negative-quantity.md) — credit `90 → 140`.
- [evidence/03-mass-assignment-put.md](evidence/03-mass-assignment-put.md) — credit `130 → 1130`.
- [evidence/pytest-vulnerable-run.txt](evidence/pytest-vulnerable-run.txt) — output pytest thật.

## 7. Phân tích nguyên nhân

- **Điểm kiểm soát bị thiếu/sai:**
  - `services/workshop/crapi/shop/views.py` (POST): chỉ kiểm tra
    `available_credit < product.price` mà không nhân với `quantity` và không yêu cầu
    `quantity >= 1`; sau đó trừ `price * quantity`, nên `quantity` âm làm tăng credit.
  - `views.py` (PUT): đọc `request_data`, gán trực tiếp `order.quantity` từ client; nếu
    body có `status` hợp lệ và khác trạng thái hiện tại thì gán `order.status`; khi
    `status == "returned"` thì hoàn `order.quantity * price` — dùng luôn `quantity` vừa bị
    client sửa.
  - `serializers.py::ProductQuantitySerializer` chỉ khai báo `product_id`, `quantity`,
    nhưng view PUT không dùng serializer này để lọc input mà đọc thẳng `status` — trường
    không có trong schema tài liệu.
- **Lớp cần khắc phục:** API/Service (validation + allowlist + phân quyền thuộc tính);
  database nên lưu snapshot giá/quantity tại thời điểm mua để tính hoàn tiền.
- **Phạm vi tác động đã chứng minh:** cùng một người dùng hợp lệ có thể tăng credit từ
  `$130` lên `$1130` chỉ bằng một request PUT, không cần hoàn hàng; có thể lặp lại.
- **Những điều chưa chứng minh:** chưa kiểm chứng trên bản đã vá; chưa khai thác chuỗi
  qua UI/QR thật; chưa đánh giá ảnh hưởng sang các service khác.

## 8. Biện pháp khắc phục

- **Allowlist field:** POST/PUT chỉ nhận `product_id`, `quantity`; từ chối (hoặc bỏ qua
  và log) mọi trường khác, đặc biệt `status`, `transaction_id`, `user`, `credit`.
- **Validation nghiệp vụ:** `quantity` là số nguyên `>= 1` và có giới hạn trên; kiểm tra
  `price * quantity <= available_credit` trước khi trừ; tính tiền hoàn toàn phía server.
- **Tách luồng hoàn tiền:** không cho client đặt `status`; refund chỉ qua endpoint riêng
  dành cho quy trình cửa hàng, kiểm tra trạng thái đơn thực tế và tính hoàn tiền từ
  snapshot `price`/`quantity` lúc mua, không từ giá trị mutable.
- **Phòng thủ bổ sung:** giao dịch DB + idempotency cho refund, audit log, kiểm tra quyền
  sở hữu đơn, test hồi quy cho cả hai vector.
- **Kiểm thử lại sau sửa:** hai test trong `tests/security/test_mass_assignment.py` phải
  PASS trên bản đã vá (khi đó mới được kết luận đã khắc phục).

## 9. Automated security test

- **File:** `tests/security/test_mass_assignment.py` (marker `security`, bỏ `skip`).
- **Tiền điều kiện:** crAPI local tại `CRAPI_BASE_URL` (mặc định
  `http://127.0.0.1:8888`); test tự đăng ký tài khoản mới nên không cần seed thủ công.
- **Kết quả mong đợi trên vulnerable target:** cả hai test **FAIL**, vì crAPI chấp nhận
  thuộc tính server-owned.
- **Kết quả thực tế:**
  - `test_order_rejects_non_positive_quantity`: FAIL — HTTP `200`, credit `100.0 → 150.0`.
  - `test_client_cannot_override_protected_refund_fields`: FAIL — HTTP `200`,
    credit `90.0 → 1090.0`, response trả `quantity=100`, `status=returned`.
- **Ý nghĩa PASS/FAIL/SKIP:**
  - `FAIL` trên crAPI = phát hiện lỗ hổng có thể tái hiện, không phải lỗi mạng/setup.
  - `PASS` chỉ có ý nghĩa "đã khắc phục" khi chạy trên phiên bản thực sự đã vá.
  - `SKIP` đã được bỏ cho các case hoàn thành.

## 10. Kết luận và tham khảo

- **Kết luận:** crAPI tin tưởng dữ liệu client ở workflow đơn hàng, cho phép thay đổi
  `quantity`/`status` (thuộc tính server quản lý) để tạo đơn âm hoặc hoàn tiền cho hàng
  chưa trả. Bằng chứng thực nghiệm cho thấy credit tăng `$1000` chỉ với một request PUT.
- **Tham khảo:**
  - OWASP API Security Top 10 2023 — API3: Broken Object Property Level Authorization.
  - OWASP API Security Top 10 2019 — API6: Mass Assignment.
  - OWASP crAPI `docs/challenges.md` (Challenge 8) và `docs/challengeSolutions.md`, repo
    `OWASP/crAPI`, commit `700f03d`.
