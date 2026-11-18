# LAB-05 — Báo cáo Unauthenticated Access

> Thực hiện: Hary Nguyenex. Nhánh `lab/05-unauthenticated-access`.
> Chỉ kiểm thử trên crAPI local do nhóm tự triển khai.

## 1. Mục tiêu và phạm vi

- **OWASP API Security category:** API2:2023 — Broken Authentication (tương ứng
  API2:2019 — Broken User Authentication).
- **crAPI challenge:** #14 — Find an endpoint that does not perform authentication checks
  for a user.
- **Tác động cần kiểm chứng:** client không cần đăng nhập (không gửi `Authorization`
  header hoặc gửi Bearer token không hợp lệ) vẫn có thể đọc trực tiếp chi tiết đơn hàng
  cùng thông tin cá nhân (email, số điện thoại) của người mua qua endpoint
  `GET /workshop/api/shop/orders/{order_id}`.

## 2. Lý thuyết

- **Khái niệm:** Unauthenticated Access xảy ra khi một API nghiệp vụ xử lý dữ liệu riêng tư
  hoặc tác vụ nội bộ nhưng bỏ sót bước xác minh danh tính người gọi (Authentication).
  Theo chuẩn HTTP (RFC 9110), cần phân biệt rõ hai mã phản hồi:
  - `401 Unauthorized`: yêu cầu chưa được xác thực danh tính (thiếu token, sai chữ ký
    hoặc token hết hạn).
  - `403 Forbidden`: đã xác thực danh tính hợp lệ nhưng tài khoản không có quyền truy cập
    tài nguyên hoặc chức năng đó.
- **Nguyên nhân thường gặp:**
  - Cấu hình framework theo chế độ mặc định mở (`AllowAny`), buộc lập trình viên phải gắn
    decorator xác thực thủ công cho từng phương thức và dẫn tới bỏ sót.
  - Gắn kiểm tra xác thực rời rạc trên `POST`/`PUT` nhưng quên gắn trên `GET` trong cùng
    một controller/view.
  - API Gateway chỉ định tuyến thuần túy vào microservice mà không kiểm tra JWT tập trung.
  - Giao diện frontend (React SPA) luôn tự động đính kèm `Authorization: Bearer <token>`,
    khiến kiểm thử chức năng qua trình duyệt luôn trả `200 OK` và che khuất lỗi thiếu kiểm
    tra ở backend.
- **Biện pháp phòng chống:** áp dụng chính sách xác thực tập trung theo nguyên tắc
  *Deny-by-Default* (mặc định yêu cầu đăng nhập cho toàn bộ API, chỉ mở allowlist tường
  minh cho các route công khai như `/login`, `/signup`, `/health`); kết hợp kiểm tra quyền
  sở hữu đối tượng sau bước xác thực và bổ sung regression test cho mọi endpoint bảo vệ.

## 3. Môi trường thực nghiệm

- **crAPI:** phiên bản `1.1.5`, commit `700f03d12a392d9e408260b4beae72ed02a4a1a4`
  (OWASP/crAPI, chạy bằng `bash scripts/crapi.sh up`).
- **Công cụ:** Windows (PowerShell / Git Bash), Docker Compose, Python `3.11.0`,
  `pytest 9.2.0`, `httpx 0.28.1`, `python-dotenv 1.2.4`, Chrome DevTools / Burp Suite.
- **Điều kiện ban đầu:** một tài khoản thử nghiệm do test tự đăng ký ngẫu nhiên trong
  local crAPI, credit khởi tạo `$100`, tạo 01 đơn hàng mẫu (`Seat`, giá `$10`) để có
  `order_id` hợp lệ. Không ghi credentials/token thật vào repo.

## 4. Khảo sát chức năng bình thường

- **Mục đích nghiệp vụ:** người dùng sau khi đăng nhập vào Shop có thể mua phụ tùng xe,
  xem danh sách lịch sử mua hàng (**Past Orders**) và tra cứu chi tiết từng đơn hàng cụ thể
  theo `order_id`. Trên giao diện web (`services/web/src/sagas/shopSaga.ts::getOrderById`),
  frontend luôn gửi kèm header `Authorization: Bearer <JWT>`.
- **Endpoint liên quan:**
  - `GET /workshop/api/shop/products` — lấy danh sách sản phẩm và số dư credit hiện tại
    (yêu cầu JWT).
  - `POST /workshop/api/shop/orders` — tạo đơn hàng mới, body
    `{"product_id":1,"quantity":1}` (yêu cầu JWT).
  - `GET /workshop/api/shop/orders/all` — lấy danh sách đơn hàng của người dùng hiện tại
    (endpoint đối chứng, có `@jwt_auth_required`).
  - `GET /workshop/api/shop/orders/{order_id}` — lấy chi tiết một đơn hàng theo ID
    (endpoint mục tiêu của Challenge #14, bị thiếu kiểm tra xác thực).
- **Request/response hợp lệ:** khi gửi kèm `Authorization: Bearer <JWT redacted>`,
  `GET /workshop/api/shop/orders/{order_id}` trả `HTTP 200 OK` gồm đối tượng `order`
  (`id`, `user.email`, `user.number`, `product`, `quantity`, `status`, `transaction_id`)
  và `payment`.

## 5. Phương pháp kiểm thử

1. **Khởi tạo dữ liệu:** đăng ký tài khoản thử nghiệm mới với email/số điện thoại ngẫu
   nhiên (`tests/security/test_unauthenticated_access.py::_signup_and_login`), đăng nhập
   lấy JWT và tạo 01 đơn hàng mẫu để nhận `order_id`.
2. **Kiểm thử có kiểm soát:**
   - Đối chứng (Control): gọi `GET /workshop/api/shop/orders/all` không có `Authorization`
     header để xác nhận cơ chế chặn `401 Unauthorized` đang hoạt động trên cùng phân hệ.
   - Vector A (Missing token): gọi `GET /workshop/api/shop/orders/{order_id}` hoàn toàn
     không có `Authorization` header và không có cookie.
   - Vector B (Invalid token): gọi `GET /workshop/api/shop/orders/{order_id}` với header
     giả mạo `Authorization: Bearer invalid.jwt.token`.
3. **Dấu hiệu xác nhận:** endpoint đối chứng trả `401`, trong khi cả hai vector trên
   `GET /workshop/api/shop/orders/{order_id}` đều trả `HTTP 200 OK` kèm đầy đủ thông tin
   đơn hàng và PII của người mua (`order.user.email`, `order.user.number`).
4. **Cách chạy lại:**
   ```bash
   bash scripts/crapi.sh up
   source .venv/Scripts/activate
   pytest tests/security/test_unauthenticated_access.py -v
   ```

## 6. Bằng chứng

Tất cả request/response được làm sạch JWT, email và số điện thoại tài khoản thử tại thư
mục [evidence/](evidence/README.md) *(cập nhật file capture và output chạy thật ngay sau
khi khởi chạy cụm container Docker local)*:

- `evidence/01-normal-flow.md` — luồng đăng nhập, tạo đơn và xem đơn hợp lệ có JWT.
- `evidence/02-control-orders-all-401.md` — đối chứng `GET /workshop/api/shop/orders/all`
  không có token bị từ chối `401 Unauthorized`.
- `evidence/03-unauthenticated-order-detail.md` — truy cập `GET /workshop/api/shop/orders/{order_id}`
  không cần token và với token sai định dạng vẫn nhận `200 OK`.
- `evidence/pytest-vulnerable-run.txt` — output chạy thật của bộ test trên crAPI local.

## 7. Phân tích nguyên nhân

- **Điểm kiểm soát bị thiếu/sai:**
  - `services/workshop/crapi/shop/views.py` (`OrderControlView`): các phương thức `post`
    (dòng 167) và `put` (dòng 218) đều gắn decorator `@jwt_auth_required` (và `OrderDetailsView.get`
    cho `/orders/all` ở dòng 267 cũng gắn `@jwt_auth_required`), nhưng phương thức `get`
    (dòng 109) xử lý `GET /workshop/api/shop/orders/{order_id}` bị bỏ quên hoàn toàn
    `@jwt_auth_required` dù docstring dòng 114 ghi rõ yêu cầu JWT.
  - `services/workshop/crapi_site/settings.py` (dòng 128–136): cấu hình `REST_FRAMEWORK`
    không khai báo `DEFAULT_AUTHENTICATION_CLASSES` và `DEFAULT_PERMISSION_CLASSES`, nên
    Django REST Framework mặc định áp dụng `AllowAny` cho mọi APIView không gắn decorator.
  - `services/web/nginx.conf.template` (dòng 165–181): Nginx reverse proxy chuyển tiếp
    thẳng `/workshop/` vào microservice mà không xác thực JWT tại tầng Gateway.
- **Lớp cần khắc phục:** tầng Framework/Middleware của microservice `workshop` (xác thực
  tập trung mặc định) kết hợp tầng Controller/View (kiểm tra quyền sở hữu đơn hàng).
- **Phạm vi tác động đã chứng minh:** qua đối chiếu mã nguồn commit `700f03d` (và kịch bản
  kiểm thử tự động), người gọi không cần tài khoản hợp lệ vẫn đọc được chi tiết đơn hàng,
  `transaction_id`, `email` và `number` của người mua qua ID đơn hàng dạng số nguyên tuần tự.
- **Những điều chưa chứng minh:** các thao tác ghi/sửa đổi đơn hàng (`POST`, `PUT`) vẫn có
  `@jwt_auth_required` nên người dùng ẩn danh không thể tạo hoặc hoàn đơn qua lỗ hổng này;
  chưa kiểm chứng trên bản đã vá; cần đính kèm thêm log thực thi trực tiếp từ Docker local.

## 8. Biện pháp khắc phục

- **Bổ sung xác thực và phân quyền tại View:** gắn `@jwt_auth_required` cho
  `OrderControlView.get`, bắt ngoại lệ `Order.DoesNotExist` trả `404`, đồng thời kiểm tra
  `if user != order.user:` trả `403 Forbidden` để ngăn chặn luôn lỗi BOLA sau khi đăng nhập.
- **Xác thực tập trung (Deny-by-Default):** chuyển logic kiểm tra JWT trong
  `services/workshop/utils/jwt.py` thành lớp `BaseAuthentication` của DRF và cấu hình
  `DEFAULT_PERMISSION_CLASSES = ["rest_framework.permissions.IsAuthenticated"]` trong
  `settings.py`; chỉ mở `AllowAny` tường minh cho healthcheck hoặc endpoint công khai.
- **Tối thiểu hóa dữ liệu và ẩn định danh:** tránh trả thừa số điện thoại/email đầy đủ
  trong chi tiết đơn hàng nếu giao diện không cần thiết; cân nhắc dùng UUID thay cho ID
  nguyên tự tăng.
- **Kiểm thử lại sau sửa:** chạy lại `pytest tests/security/test_unauthenticated_access.py -v`;
  cả ba test phải `PASSED` trên phiên bản đã áp dụng bản vá (khi đó mới kết luận đã khắc phục).

## 9. Automated security test

- **File:** `tests/security/test_unauthenticated_access.py` (marker `security`, bỏ `skip`).
- **Tiền điều kiện:** crAPI local chạy tại `CRAPI_BASE_URL` (mặc định
  `http://127.0.0.1:8888`); test tự đăng ký tài khoản thử và tự tạo đơn hàng mẫu nên không
  cần seed thủ công.
- **Kết quả mong đợi trên vulnerable target:**
  - `test_orders_list_rejects_requests_without_token`: **PASS** — endpoint đối chứng
    `/workshop/api/shop/orders/all` từ chối đúng với HTTP `401`.
  - `test_protected_endpoint_rejects_requests_without_token`: **FAIL** — endpoint
    `/workshop/api/shop/orders/{order_id}` trả HTTP `200` kèm dữ liệu đơn hàng thay vì `401`.
  - `test_protected_endpoint_rejects_invalid_bearer_token`: **FAIL** — endpoint bỏ qua
    Bearer token sai định dạng và vẫn trả HTTP `200` thay vì `401`.
- **Kết quả thực tế:** sẽ đính kèm output chạy thật tại `evidence/pytest-vulnerable-run.txt`
  ngay khi hoàn tất khởi chạy Docker local.
- **Ý nghĩa PASS/FAIL/SKIP:**
  - `FAIL` trên 2 case mục tiêu của crAPI = xác nhận lỗ hổng thiếu kiểm tra xác thực có thể
    tái hiện tự động.
  - `PASS` ở case đối chứng xác nhận môi trường và cơ chế JWT của hệ thống đang hoạt động;
    2 case mục tiêu chỉ `PASS` khi chạy trên bản thực sự đã vá.
  - `SKIP` đã được gỡ bỏ cho các test case hoàn chỉnh.

## 10. Kết luận và tham khảo

- **Kết luận:** microservice `workshop` của crAPI không áp dụng cơ chế xác thực mặc định
  toàn cục và bỏ sót `@jwt_auth_required` tại `OrderControlView.get`, cho phép truy vấn
  `GET /workshop/api/shop/orders/{order_id}` mà không cần đăng nhập, dẫn tới lộ thông tin
  giao dịch và PII của người dùng.
- **Tham khảo:**
  - OWASP API Security Top 10 2023 — API2:2023 Broken Authentication.
  - OWASP API Security Top 10 2019 — API2:2019 Broken User Authentication.
  - IETF RFC 9110 — HTTP Semantics (`401 Unauthorized` & `403 Forbidden`).
  - OWASP crAPI `docs/challenges.md` (Challenge 14) và `services/workshop/crapi/shop/views.py`,
    repo `OWASP/crAPI`, commit `700f03d`.
