# LAB-01 — Báo cáo BOLA

## 1. Mục tiêu và phạm vi

- **OWASP API Security category:** API1:2023 — Broken Object Level Authorization (BOLA).
- **crAPI challenge:** Challenge #1 — Truy cập trái phép thông tin/vị trí phương tiện của người dùng khác thông qua định danh đối tượng (`vehicle_id`).
- **Tác động cần kiểm chứng:** Kiểm chứng khả năng một người dùng đã xác thực hợp lệ (User A) có thể truy vấn và đọc dữ liệu tọa độ GPS cùng thông tin cá nhân gắn với phương tiện thuộc sở hữu của người dùng khác (User B) bằng cách thay đổi tham số `{vehicle_id}` trên endpoint quản lý vị trí xe trong môi trường lab cục bộ.

## 2. Lý thuyết

- **Khái niệm:** Broken Object Level Authorization (BOLA) là lỗ hổng xảy ra khi một API nhận định danh đối tượng (Object ID) do phía client truyền vào (qua path parameter, query string hoặc request body) nhưng không kiểm tra xem người dùng đang thực hiện yêu cầu có quyền sở hữu hoặc quyền truy cập đối với đối tượng cụ thể đó hay không.
- **Nguyên nhân thường gặp:**
  - Lập trình viên chỉ kiểm tra bước xác thực (Authentication — xác minh JWT token hoặc session hợp lệ) mà bỏ qua bước kiểm tra phân quyền ở mức đối tượng (Object-level Authorization).
  - Truy vấn trực tiếp bản ghi trong cơ sở dữ liệu chỉ dựa trên `object_id` do client cung cấp mà không ràng buộc thêm điều kiện `owner_id = current_user_id`.
  - Việc sử dụng định danh dạng UUID nhưng để lộ công khai các UUID này ở những API khác (như bảng tin Community) tạo điều kiện cho kẻ tấn công thu thập định danh mục tiêu.
- **Biện pháp phòng chống:**
  - Thực thi kiểm tra quyền sở hữu ở tầng nghiệp vụ (Service/Controller) cho mọi thao tác đọc/ghi/xóa đối tượng, đối chiếu `owner_id` của tài nguyên với `user_id` được trích xuất từ JWT đã xác thực ở phía server.
  - Truy vấn dữ liệu theo cặp điều kiện `(object_id, owner_id)` ngay tại tầng truy xuất dữ liệu (Repository/Database).
  - Tránh trả về định danh nội bộ nhạy cảm của tài nguyên (như `vehicleid`) trong các API công khai không cần thiết.

## 3. Môi trường thực nghiệm

- **Git commit hoặc phiên bản crAPI:** `700f03d12a392d9e408260b4beae72ed02a4a1a4` (nhánh làm việc: `lab/bola`).
- **Công cụ, phiên bản:**
  - Hệ điều hành & ảo hóa: Windows 10 (64-bit), Docker Desktop (WSL 2 backend), chế độ `CRAPI_MINIMAL=1` (`crapi-web`, `crapi-workshop`, `mailhog`, `mongodb`, `postgresdb`).
  - Trình duyệt & CLI: Google Chrome DevTools (tab Network), Git Bash (`curl`).
  - Môi trường kiểm thử tự động: `Python 3.12.3`, `pytest 9.2.0`, `httpx 0.28.1`, `python-dotenv 1.2.4`.
- **Tài khoản thử nghiệm/điều kiện ban đầu (không ghi credentials):**
  - **User A (tài khoản kiểm thử truy vấn chéo):** Đăng ký cục bộ trên crAPI, kích hoạt thành công 01 phương tiện riêng qua mã VIN và Pincode nhận từ MailHog (UUID xe của User A: `22a84d75-033d-46b6-9d9f-8a92cf98ffb6`).
  - **User B (tài khoản sở hữu tài nguyên mục tiêu):** Đăng ký độc lập cục bộ trên crAPI, kích hoạt 01 phương tiện riêng qua MailHog (UUID xe của User B: `3393b735-bb2b-4ecd-bfca-94055df20814`) và đăng 01 bài viết công khai (`"Test post B"`) trên mục Community.

## 4. Khảo sát chức năng bình thường

- **Mục đích nghiệp vụ của API:** Cho phép người dùng đã đăng nhập xem danh sách phương tiện thuộc sở hữu của mình và cập nhật/truy vấn tọa độ vị trí GPS hiện tại của phương tiện trên bản đồ Dashboard.
- **Endpoint và method liên quan:**
  - `GET /identity/api/v2/vehicle/vehicles` — Lấy danh sách phương tiện gắn với tài khoản đang đăng nhập.
  - `GET /identity/api/v2/vehicle/{vehicle_id}/location` — Truy vấn tọa độ GPS (`latitude`, `longitude`) và thông tin định danh của phương tiện theo `{vehicle_id}`.
- **Cơ chế xác thực & tham số đầu vào:**
  - Client gửi kèm JWT access token trong HTTP Request Header: `Authorization: Bearer <JWT_TOKEN>`.
  - Tham số đường dẫn (Path parameter): `{vehicle_id}` là chuỗi định danh UUID của phương tiện (ví dụ với User A: `22a84d75-033d-46b6-9d9f-8a92cf98ffb6`).
- **Request/response hợp lệ:** Response hợp lệ (HTTP `200 OK`) khi User A truy vấn xe của chính mình:
```json
{
  "carId": "22a84d75-033d-46b6-9d9f-8a92cf98ffb6",
  "vehicleLocation": {
    "id": 2,
    "latitude": "31.284788",
    "longitude": "-92.471176"
  },
  "fullName": "User A",
  "email": "<REDACTED_EMAIL>"
}
```
## 5. Phương pháp kiểm thử

1. **Các bước khởi tạo dữ liệu:**
   - Khởi động môi trường crAPI cục bộ tại `http://127.0.0.1:8888` và MailHog tại `http://127.0.0.1:8025`.
   - Tạo lần lượt 02 tài khoản độc lập (User A và User B), lấy cặp mã VIN và Pincode từ MailHog để kích hoạt phương tiện riêng cho từng tài khoản.
   - Sử dụng phiên đăng nhập của User B đăng một bài viết mới trên diễn đàn **Community** để tạo dữ liệu công khai.
2. **Các bước kiểm thử có kiểm soát trong Lab:**
   - Đăng nhập bằng **User A**, mở Chrome DevTools $\rightarrow$ **Network** $\rightarrow$ **Fetch/XHR** và truy cập mục **Community**.
   - Quan sát gói tin `GET /community/api/v2/community/posts/recent`, ghi nhận chuỗi `vehicleid` của User B (`3393b735-bb2b-4ecd-bfca-94055df20814`) bị trả về công khai trong đối tượng `author` của bài viết.
   - Sử dụng `curl` gửi yêu cầu `GET /identity/api/v2/vehicle/3393b735-bb2b-4ecd-bfca-94055df20814/location` với header `Authorization: Bearer <TOKEN_CUA_USER_A>`.
3. **Dấu hiệu để xác nhận hành vi sai quyền/bất thường:**
   - Về mặt chính sách bảo mật chuẩn, máy chủ phải từ chối yêu cầu truy cập chéo đối tượng bằng mã trạng thái HTTP `401`, `403` hoặc `404`.
   - Dấu hiệu xác nhận tồn tại lỗ hổng BOLA: Máy chủ trả về mã **`HTTP/1.1 200`** cùng nội dung JSON chứa tọa độ GPS, tên và địa chỉ email của User B cho phiên của User A.
4. **Cách chạy lại bằng test Python:**
   - Đảm bảo stack Docker của crAPI đang hoạt động ở trạng thái `healthy`, cài đặt thư viện từ `requirements.txt` và chạy lệnh: `pytest tests/security/test_bola.py -v`.

## 6. Bằng chứng

Toàn bộ ảnh bằng chứng đã được làm sạch (che kín chuỗi JWT token và địa chỉ email) và lưu trong thư mục `labs/01-bola/evidence/`:

1. **[`evidence/01-community-vehicleid-exposure.png`](evidence/01-community-vehicleid-exposure.png):** Kết quả response từ endpoint `GET /community/api/v2/community/posts/recent` khi đăng nhập bằng User A, cho thấy API bảng tin công khai trả về trực tiếp trường `"vehicleid": "3393b735-bb2b-4ecd-bfca-94055df20814"` trong thông tin tác giả bài viết của User B.
2. **[`evidence/02-bola-unauthorized-vehicle-read.png`](evidence/02-bola-unauthorized-vehicle-read.png):** Kết quả kiểm chứng bằng `curl` khi gửi yêu cầu `GET /identity/api/v2/vehicle/3393b735-bb2b-4ecd-bfca-94055df20814/location` kèm token xác thực của User A; máy chủ phản hồi mã `HTTP/1.1 200` và trả về đầy đủ dữ liệu tọa độ GPS (`latitude`, `longitude`), `fullName` và `email` của User B.

## 7. Phân tích nguyên nhân

- **Điểm kiểm soát bảo mật bị thiếu/sai:**
  - Tại endpoint `GET /identity/api/v2/vehicle/{vehicle_id}/location`, dịch vụ `identity-service` chỉ xác thực chữ ký và thời hạn của JWT token (kiểm tra người gọi đã đăng nhập hay chưa) mà hoàn toàn không đối chiếu quyền sở hữu giữa `user_id` trong JWT với chủ sở hữu của `{vehicle_id}` được truyền trên URL.
  - Đồng thời, endpoint `GET /community/api/v2/community/posts/recent` của `community-service` trả về trường định danh `vehicleid` của tác giả bài viết ra giao diện công khai, giúp bất kỳ người dùng nào cũng có thể thu thập được định danh xe của người khác.
- **Lớp cần khắc phục (API/Service/Database):**
  - **Tầng Service / Controller (`identity-service`):** Bắt buộc bổ sung logic xác minh quyền sở hữu tài nguyên trước khi trả dữ liệu vị trí phương tiện.
  - **Tầng Database / Repository:** Truy vấn thông tin phương tiện theo điều kiện kết hợp cả định danh xe và định danh chủ sở hữu (`WHERE uuid = :vehicle_id AND owner_id = :current_user_id`).
  - **Tầng DTO / Serializer (`community-service`):** Loại bỏ trường `vehicleid` khỏi payload phản hồi của API bảng tin công khai.
- **Phạm vi tác động đã chứng minh:**
  - Người dùng đã xác thực bất kỳ có thể đọc trái phép tọa độ vị trí GPS (`latitude`, `longitude`), tên hiển thị (`fullName`) và địa chỉ `email` gắn với phương tiện của người dùng khác.
- **Những điều chưa chứng minh:**
  - Chưa kiểm thử các thao tác ghi/sửa/xóa trái phép trên tài nguyên phương tiện của người khác (như thay đổi trạng thái hoặc lệnh điều khiển xe) do phạm vi Lab 01 giới hạn ở luồng truy vấn đọc thông tin vị trí xe.

## 8. Biện pháp khắc phục

- **Cách sửa được đề xuất:**
  1. **Kiểm tra quyền sở hữu ở tầng nghiệp vụ (`identity-service`):** Khi xử lý yêu cầu `GET /identity/api/v2/vehicle/{vehicle_id}/location`, trích xuất định danh người dùng hiện tại (`currentUserId`) từ `SecurityContext` / JWT đã xác thực, sau đó kiểm tra bản ghi `Vehicle` tương ứng với `vehicle_id` có thuộc về `currentUserId` hay không. Nếu không khớp, trả về ngay mã `403 Forbidden` (hoặc `404 Not Found` để tránh lộ sự tồn tại của tài nguyên).
  2. **Ràng buộc truy vấn ở tầng dữ liệu:** Thay thế các truy vấn chỉ tìm theo `vehicle_id` bằng truy vấn gắn liền chủ sở hữu (ví dụ `findByUuidAndOwnerId(vehicleId, currentUserId)`).
  3. **Giảm thiểu dữ liệu lộ lọt (Data Minimization) ở `community-service`:** Lược bỏ trường `vehicleid` khỏi đối tượng `author` khi tuần tự hóa dữ liệu bài viết trả về cho endpoint `/community/api/v2/community/posts/recent`.
- **Kiểm thử lại sau sửa:**
  - Sau khi áp dụng bản vá và khởi động lại dịch vụ `identity-service`, chạy lại lệnh `pytest tests/security/test_bola.py -v`.
  - Bản vá đạt yêu cầu khi endpoint `GET /identity/api/v2/vehicle/{vehicle_id_B}/location` (gọi bằng token của User A) trả về mã HTTP `403` hoặc `404`, không chứa dữ liệu vị trí/email của User B, và bài kiểm thử tự động chuyển từ `FAILED` sang `PASSED`.

## 9. Automated security test

- **File Python test:** `tests/security/test_bola.py` (hàm `test_user_cannot_read_another_users_vehicle`, sử dụng fixture `api_client` trong `tests/conftest.py` trỏ tới `http://127.0.0.1:8888`).
- **Tiền điều kiện:**
  - Các container crAPI chạy cục bộ ở trạng thái `healthy`.
  - Đã cài đặt đầy đủ các gói trong `requirements.txt` (`pytest`, `httpx`, `python-dotenv`).
  - Hai tài khoản thử nghiệm User A và User B (cấu hình qua biến môi trường `CRAPI_USER_A_EMAIL`, `CRAPI_USER_A_PASSWORD`, `CRAPI_USER_B_EMAIL`, `CRAPI_USER_B_PASSWORD` hoặc giá trị mặc định cục bộ của lab) đã tồn tại và kích hoạt phương tiện riêng.
- **Kết quả mong đợi trên vulnerable target:**
  - Bài kiểm thử khẳng định chính sách an toàn `assert unauthorized_resp.status_code in {401, 403, 404}`. Trên phiên bản crAPI chưa vá lỗi, bài test sẽ kết thúc với trạng thái **`FAILED`** tại dòng `AssertionError` do server trả về mã `200` kèm dữ liệu phương tiện của User B.
- **Kết quả thực tế:**
  - Thực thi lệnh `pytest tests/security/test_bola.py -v` trên commit `700f03d12a392d9e408260b4beae72ed02a4a1a4` cho kết quả `1 failed in 4.05s` (đã làm sạch địa chỉ email trong log):
    - `tests/security/test_bola.py::test_user_cannot_read_another_users_vehicle FAILED [100%]`
    - `AssertionError: BOLA detected: expected 401/403/404 when User A reads User B's vehicle (3393b735-bb2b-4ecd-bfca-94055df20814), but got 200: {"carId":"3393b735-bb2b-4ecd-bfca-94055df20814","vehicleLocation":{"id":2,"latitude":"31.284788","longitude":"-92.471176"},"fullName":"User B","email":"<REDACTED_EMAIL>"}`
    - `assert 200 in {401, 403, 404}`
- **Ý nghĩa PASS/FAIL/SKIP:**
  - **`FAILED`:** Hệ thống mục tiêu đang tồn tại lỗ hổng BOLA — máy chủ cho phép tài khoản A đọc trái phép tài nguyên phương tiện của tài khoản B (`HTTP 200`) thay vì từ chối theo chính sách phân quyền.
  - **`PASSED`:** Máy chủ đã kiểm tra quyền sở hữu đối tượng đúng chuẩn và từ chối yêu cầu truy cập trái phép bằng mã trạng thái `401`, `403` hoặc `404`.
  - **`SKIP`:** Bài kiểm thử chưa được kích hoạt hoặc môi trường mục tiêu chưa sẵn sàng để chạy kiểm tra hồi quy.

## 10. Kết luận và tham khảo

- **Kết luận dựa trên bằng chứng:**
  - Qua quá trình khảo sát thực nghiệm và chạy kiểm thử tự động trên crAPI (commit `700f03d12a392d9e408260b4beae72ed02a4a1a4`), đã chứng minh chắc chắn sự tồn tại của lỗ hổng **Broken Object Level Authorization (OWASP API1:2023)** tại endpoint `GET /identity/api/v2/vehicle/{vehicle_id}/location`. Kết hợp với việc `GET /community/api/v2/community/posts/recent` để lộ `vehicleid` của tác giả bài viết, bất kỳ người dùng đã đăng nhập nào cũng có thể thu thập định danh xe và truy xuất trái phép vị trí GPS cùng email của người dùng khác.
- **Tài liệu OWASP/API Security/nguồn chính thức:**
  - OWASP API Security Top 10 (2023) — *API1:2023 Broken Object Level Authorization*: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
  - OWASP crAPI (Completely Ridiculous API) Official Repository & Challenges Documentation: https://github.com/OWASP/crAPI