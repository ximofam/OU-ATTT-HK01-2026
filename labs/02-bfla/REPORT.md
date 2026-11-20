LAB-02 — Broken Function Level Authorization (BFLA)
Challenge: crAPI #7 — Delete a video of another user
OWASP API Security: API5:2023 — Broken Function Level Authorization
1. Mục tiêu và phạm vi
•	OWASP API Security category: API5:2023 — Broken Function Level Authorization (BFLA).
•	crAPI challenge: #7 — Delete a video of another user.
•	Tác động cần kiểm chứng: Tài khoản có quyền thông thường có thể gọi chức năng quản trị để xóa video của tài khoản khác hay không.
•	Phạm vi: Chỉ thử nghiệm trên môi trường crAPI chạy local và dữ liệu giả do nhóm tạo. Không kiểm thử hệ thống bên ngoài.
2. Lý thuyết
Khái niệm
BFLA là lỗi xảy ra khi ứng dụng không kiểm tra đúng quyền của người dùng đối với một chức năng hoặc endpoint. Người dùng đã đăng nhập nhưng không có vai trò phù hợp vẫn có thể gọi chức năng dành cho vai trò cao hơn.
Phân biệt BFLA và BOLA
•	BFLA: Kiểm tra quyền thực hiện một chức năng. Ví dụ: tài khoản USER gọi chức năng xóa video dành cho ADMIN.
•	BOLA: Kiểm tra quyền truy cập một đối tượng cụ thể. Ví dụ: người dùng sửa hoặc xem dữ liệu thuộc về người dùng khác bằng cách thay đổi ID đối tượng.
Trong Lab này, trọng tâm là việc tài khoản USER gọi được endpoint quản trị xóa video, do đó thuộc BFLA. Việc video thuộc tài khoản khác là đối tượng được dùng để kiểm chứng tác động.
Nguyên nhân thường gặp
•	Backend chỉ kiểm tra người dùng đã đăng nhập mà không kiểm tra role.
•	Endpoint đặc quyền không có kiểm tra quyền ở tầng controller hoặc service.
•	Ứng dụng dựa vào việc ẩn chức năng trên giao diện thay vì kiểm soát tại server.
Biện pháp phòng chống
•	Kiểm tra quyền ở phía server cho từng chức năng đặc quyền.
•	Áp dụng nguyên tắc đặc quyền tối thiểu.
•	Kiểm tra quyền sở hữu đối tượng khi nghiệp vụ yêu cầu.
•	Viết automated security test để ngăn lỗi tái xuất hiện.
3. Môi trường thực nghiệm
•	Ứng dụng: OWASP crAPI chạy local bằng Docker Compose.
•	Địa chỉ API: http://127.0.0.1:8888.
•	Công cụ: Docker Compose, Git Bash trên Windows, Python, pytest.
•	Tài khoản thử nghiệm:
o	testerlab: ROLE_USER, user_id = 9.
o	ownerlab: ROLE_USER, user_id = 8.
•	Dữ liệu thử nghiệm: Video giả lab02-test.mp4, video_id = 6, được tạo bởi ownerlab.
•	Thông tin xác thực: Không ghi mật khẩu, JWT, cookie hoặc token vào báo cáo.
4. Khảo sát chức năng bình thường
Mục đích nghiệp vụ
crAPI cung cấp chức năng tải lên và quản lý video hồ sơ người dùng. Ngoài chức năng thông thường, backend có endpoint quản trị để xóa video.
Endpoint liên quan
Chức năng	Method	Endpoint
Tải video của người dùng	POST	/identity/api/v2/user/videos
Xóa video qua chức năng quản trị	DELETE	/identity/api/v2/admin/videos/{video_id}
Endpoint quản trị là đối tượng cần kiểm tra quyền.
Dữ liệu thử nghiệm
Video lab02-test.mp4 được tải lên bằng tài khoản ownerlab. Sau khi tải lên, dữ liệu được xác nhận trong database với video_id = 6 và user_id = 8.
Phản hồi upload ban đầu là HTTP 404 nhưng bản ghi video vẫn được tạo trong database. Vì vậy, việc xác nhận dữ liệu được thực hiện bằng cách kiểm tra database, không chỉ dựa vào HTTP response.
5. Phương pháp kiểm thử
5.1. Khởi tạo dữ liệu
1.	Khởi chạy crAPI local bằng Docker Compose.
2.	Tạo hai tài khoản thử nghiệm testerlab và ownerlab.
3.	Đăng nhập bằng ownerlab.
4.	Tạo video giả lab02-test.mp4.
5.	Xác nhận video có video_id = 6, thuộc user_id = 8.
5.2. Kiểm thử trước khi sửa
1.	Đăng nhập bằng tài khoản testerlab có vai trò ROLE_USER.
2.	Gửi yêu cầu DELETE tới:
http://127.0.0.1:8888/identity/api/v2/admin/videos/6
3.	Quan sát phản hồi HTTP.
4.	Kiểm tra database để xác nhận video của ownerlab đã bị xóa.
Kết quả thực nghiệm: Server trả HTTP 200 với phản hồi JSON có trường ok: true. Kiểm tra database sau đó cho thấy video không còn được liên kết với hồ sơ ownerlab.
Đây là bằng chứng cho thấy tài khoản USER đã thực hiện được chức năng quản trị không thuộc quyền của mình.
5.3. Dấu hiệu xác nhận BFLA
•	Người gọi là testerlab, có vai trò ROLE_USER.
•	Endpoint được gọi nằm dưới đường dẫn /admin/.
•	Yêu cầu xóa video trả HTTP 200.
•	Video thử nghiệm thuộc tài khoản khác bị xóa khỏi dữ liệu.
5.4. Chạy lại automated test
Tại thư mục gốc dự án:
pytest -q tests/security/test_bfla.py -s
Test sử dụng cấu hình môi trường tương ứng để xác thực và kiểm tra tài khoản thông thường không thể gọi chức năng quản trị sau khi đã áp dụng biện pháp khắc phục.
6. Bằng chứng
Các bằng chứng cần được lưu trong thư mục labs/02-bfla/evidence/.
Bằng chứng	Nội dung	Trạng thái
Request/response trước sửa	Yêu cầu DELETE từ USER và phản hồi HTTP 200	Cần lưu bản đã làm sạch
Database trước/sau khai thác	Video thử nghiệm bị xóa khỏi hồ sơ owner	Cần lưu ảnh hoặc bản trích xuất đã làm sạch
Kết quả retest	Pytest sau khi sửa	Đã lưu tại evidence/bfla-retest.txt ở thư mục gốc dự án
Không lưu JWT, access token, cookie, mật khẩu hoặc dữ liệu cá nhân trong bằng chứng được nộp.
7. Phân tích nguyên nhân
Điểm kiểm soát bảo mật bị thiếu
Trong ProfileController.java, endpoint quản trị:
DELETE /api/v2/admin/videos/{video_id}
không có annotation @PreAuthorize để giới hạn vai trò được phép gọi.
Trong ProfileServiceImpl.java, phương thức deleteAdminProfileVideo tìm video theo ID và thực hiện xóa nhưng không kiểm tra role ADMIN của người gọi.
Do đó, việc xác thực người dùng đã đăng nhập chưa đủ để ngăn tài khoản USER gọi chức năng quản trị.
Lớp cần khắc phục
•	Controller: Bổ sung kiểm soát quyền ở endpoint nếu sử dụng method-level authorization.
•	Security configuration: Bổ sung quy tắc phân quyền cho đường dẫn /identity/api/v2/admin/videos/**.
•	Service: Nên tiếp tục bảo đảm các thao tác nhạy cảm có kiểm tra quyền phù hợp, tránh phụ thuộc hoàn toàn vào một lớp kiểm soát.
Phạm vi tác động đã chứng minh
Trong môi trường local, tài khoản testerlab với ROLE_USER đã xóa được video thử nghiệm thuộc tài khoản ownerlab thông qua endpoint quản trị.
Không suy rộng kết quả này thành khả năng truy cập mọi chức năng ADMIN hoặc mọi dữ liệu trong hệ thống.
8. Biện pháp khắc phục
Đã bổ sung quy tắc phân quyền trong WebSecurityConfig.java:
.requestMatchers("/identity/api/v2/admin/videos/**")
    .hasRole("ADMIN")
Đồng thời cấu hình accessDeniedHandler để trả HTTP 403 với thông báo JSON khi người dùng đã xác thực nhưng không đủ quyền.
Sau khi sửa:
1.	Build lại image identity.
2.	Khởi tạo lại container crapi-identity.
3.	Chờ container chuyển sang trạng thái healthy.
4.	Chạy automated test.
Kết quả kiểm thử lại: pytest trả về 1 passed.
Điều này xác nhận kịch bản test đã đạt kết quả mong đợi sau khi áp dụng quy tắc phân quyền.
9. Automated security test
•	File test: tests/security/test_bfla.py.
•	Framework: pytest.
•	Tiền điều kiện: crAPI local đang chạy, identity service healthy và tài khoản thử nghiệm được cấu hình trong môi trường chạy test.
•	Kết quả mong đợi: Tài khoản ROLE_USER không thể thực hiện chức năng xóa video quản trị.
•	Kết quả thực tế sau sửa: 1 passed.
•	File lưu kết quả: evidence/bfla-retest.txt.
Ý nghĩa:
•	PASS: Test xác nhận hành vi từ chối truy cập trái quyền như mong đợi.
•	FAIL: Test phát hiện tài khoản thường vẫn thực hiện được chức năng đặc quyền hoặc kết quả không đúng kỳ vọng.
•	SKIP: Test không được thực hiện do thiếu điều kiện chạy; không được xem là bằng chứng đã khắc phục.
10. Kết luận và tham khảo
Kết luận
Thực nghiệm trên crAPI local đã chứng minh lỗi BFLA tại chức năng xóa video quản trị: tài khoản ROLE_USER có thể gọi endpoint quản trị và xóa video thử nghiệm của tài khoản khác.
Sau khi bổ sung quy tắc yêu cầu ROLE_ADMIN cho endpoint và triển khai lại identity service, automated test đã chạy thành công với kết quả 1 passed.
Kết luận chỉ giới hạn trong endpoint và kịch bản đã kiểm thử. Cần kiểm tra bổ sung các endpoint đặc quyền khác để đánh giá toàn diện hơn.
Tài liệu tham khảo
•	OWASP API Security Top 10 — API5:2023 Broken Function Level Authorization: https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/
•	OWASP API Security Top 10 — API1:2023 Broken Object Level Authorization: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
•	OWASP crAPI: https://github.com/OWASP/crAPI

