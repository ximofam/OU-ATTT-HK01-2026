# LAB-03 — Excessive Data Exposure

## 1. Mục tiêu và phạm vi

# OWASP API Security category: API3 - Excessive Data Exposure.

# crAPI challenge: Challenge 4 - Tìm các endpoints API làm lộ thông tin nhạy cảm của người dùng.

# Tác động cần kiểm chứng:

- API trả về các trường dữ liệu nhạy cảm không cần thiết cho chức năng nghiệp vụ.
- Người dùng hiện tại có thể nhận được thông tin thuộc tài khoản khác.
- Các thông tin nhạy cảm bị thu thập thông qua các endpoints mà không cần vượt qua cơ chế xác thực.

## 2. Lý thuyết

# Khái niệm: tình trạng API trả về dữ liệu hơn mức cần thiết cho chức năng nghiệp, làm lộ các thông tin nhạy cảm và ảnh hưởng đến quyền riêng tư của người dùng.

# Nguyên nhân thường gặp:

- API trả về toàn bộ thông tin của đối tượng:
Backend truy vấn một đối tượng trong database và tuần tự hóa toàn bộ thuộc tính thành JSON response, thay vì chỉ trả về những trường cần thiết.

- Serializer hoặc DTO chứa quá nhiều trường:
Lập trình viên đưa nhiều thuộc tính vào serializer hoặc DTO mà không đánh giá mức độ cần thiết của từng trường đối với chức năng nghiệp vụ.

- Chỉ ẩn dữ liệu ở phía frontend:
Frontend chỉ hiển thị một số trường nhất định nhưng backend vẫn gửi toàn bộ dữ liệu trong response.

- Thiếu kiểm soát quyền truy cập ở cấp thuộc tính:
Backend không phân biệt trường dữ liệu nào được phép trả về cho từng loại người dùng hoặc từng chức năng nghiệp vụ.

# Biện pháp phòng chống:

- Data Minimization:
Chỉ trả về những trường dữ liệu thực sự cần thiết cho chức năng nghiệp vụ.

- Data Minimization:
Chỉ trả về những trường dữ liệu thực sự cần thiết cho chức năng nghiệp vụ.

- Kiểm soát quyền truy cập ở cấp thuộc tính:
Xác định người dùng hoặc vai trò nào được phép truy cập từng trường dữ liệu.

# Các nhóm thông tin nhạy cảm:
- Nhóm 1: Thông tin xác thực và bảo mật
+ password
+ password_hash
+ access_token
+ refresh_token
+ reset_token
+ secret_key
+ api_key
+ private_key

- Nhóm 2: Thông tin dạng cá nhân (Personally Identifiable Information - PII)
+ email
+ phone
+ address
+ date_of_birth
+ full_name
+ national_id
+ passport_number
+ location

- Nhóm 3: Thông tin tài chính
+ credit_card_number
+ bank_account
+ balance
+ transaction_history
+ payment_details
+ billing_address

- Nhóm 4: Thông tin nội bộ và nghiệp vụ
+ internal_id
+ admin_notes
+ role
+ is_admin
+ is_verified
+ internal_status
+ moderation_status
+ metadata
+ debug_info

## 3. Môi trường thực nghiệm

# Môi trường: OWASP crAPI

# Triển khai: chạy môi trường local với Docker:
- crAPI: 127.0.0.1:8888 (với listener chạy với port: 8081)
- mailHog: 127.0.0.1:8025
- firefox: 127.0.0.1:8081

# Công cụ: Burpsuite

# Tài khoản thử nghiệm/điều kiện ban đầu (không ghi credentials):
+ Tài khoản 1: Tên người dùng: truong, Email: truong123@gmail



## 4. Khảo sát chức năng bình thường

# Mục đích nghiệp vụ của API:

- Endpoint 1: Hiển thị các thông tin liên quan đến chi tiết của xe (mechanic code).

- Endpoint 2: Hiển thị danh sách thông tin liên quan đến nội dung các bài posts (tiêu đề, nội dung, ngày đăng, tên người đăng).

- Endpoint 3: Hiển thị thông tin liên quan đến chi tiết của 1 bài post (tiêu đề, nội dung, ngày đăng, tên người dùng).

- Endpoint 4: Hiển thị thông tin liên quan đến chi tiết của 1 bài post (tiêu đề, nội dung, ngày đăng, tên người dùng) và thông tin các comments (tên người bình luận, nội dung bình luận, ngày bình luận).

- Endpoint 5: Cập nhật ảnh đại diện và hiển thị ảnh lên trang Profile cho người dùng.

- Endpoint 6: Hiển thị thông tin xe và tọa độ của xe (phục vụ cho bản đồ thời gian thực).

- Endpoint 7: Hiển thị danh sách các xe và thông tin của từng xe.

# Endpoint và method liên quan:

- Endpoint 1:
Method: GET
Path: /workshop/api/mechanic

- Endpoint 2:
Method: GET
Path: /community/api/v2/community/posts/recent

- Endpoint 3:
Method: GET
Path: /community/api/v2/community/posts/{id}

- Endpoint 4:
Method: POST
Path: /community/api/v2/community/posts/{id}/comment

- Endpoint 5:
Method: POST
Path: /identity/api/v2/user/pictures

- Endpoint 6:
Method: GET
Path: /identity/api/v2/vehicle/{id}/location

- Endpoint 7:
Method: GET
Path: /identity/api/v2/vehicle/vehicles

# Request/response hợp lệ:

- Endpoint 1:
+ Request: evidence/endpoint-01-mechanic/request.txt
+ Response: evidence/endpoint-01-mechanic/response.txt

- Endpoint 2:
+ Request: evidence/endpoint-02-recent-posts/request.txt
+ Response: evidence/endpoint-02-recent-posts/response.txt

- Endpoint 3:
+ Request: evidence/endpoint-03-post-detail/request.txt
+ Response: evidence/endpoint-03-post-detail/response.txt

- Endpoint 4:
+ Request: evidence/endpoint-04-comments/request.txt
+ Response: evidence/endpoint-04-comments/response.txt

- Endpoint 5:
+ Request: evidence/endpoint-05-user-pictures/request.txt
+ Response: evidence/endpoint-05-user-pictures/response.txt

- Endpoint 6:
+ Request: evidence/endpoint-06-vehicle-location/request.txt
+ Response: evidence/endpoint-06-vehicle-location/response.txt 

- Endpoint 7:
+ Request: evidence/endpoint-07-vehicles/request.txt
+ Response: evidence/endpoint-07-vehicles/response.txt


## 5. Phương pháp kiểm thử

# Các bước khởi tạo dữ liệu.
1. Khởi chạy các container Docker của crAPI.

2. Kiểm tra khả năng truy cập ứng dụng tại http://127.0.0.1:8888.

3. Khởi động Burp Suite và cấu hình Proxy Listener tại port 8081.

4. Cấu hình Firefox sử dụng Burp Suite làm HTTP proxy.

5. Truy cập crAPI và đăng nhập tài khoản thử nghiệm.

6. Thực hiện các thao tác nghiệp vụ tương ứng với 7 endpoints.

7. Thu thập các request/response thông qua HTTP history của Burp Suite.

# Các bước kiểm thử có kiểm soát trong Lab.
1. Xác định chức năng tương ứng trên giao diện.

2. Thực hiện thao tác nghiệp vụ bình thường.

3. Quan sát request được gửi từ frontend đến backend thông qua Burp Suite.

4. Gửi request đến Repeater để kiểm tra và quan sát response.

5. Phân tích cấu trúc JSON và xác định các trường dữ liệu được trả về.

6. Đối chiếu các trường dữ liệu với mục đích nghiệp vụ đã xác định.

7. Phân loại những trường có khả năng là dữ liệu nhạy cảm hoặc không cần thiết.

8. Lưu lại request/response làm bằng chứng.

# Cách chạy lại bằng test Python.
1. Khởi tạo HTTP client.

2. Đăng nhập tài khoản thử nghiệm và lấy JWT token.

3. Gửi request đến từng endpoint.

4. Kiểm tra HTTP status code.

5. Phân tích JSON response.

6. Duyệt đệ quy cấu trúc JSON để tìm các trường dữ liệu thuộc danh sách kiểm tra.

7. Phân loại kết quả dựa trên mức độ rủi ro.

8. Xuất kết quả thông qua pytest.

## 6. Bằng chứng

Đặt ảnh và request/response đã làm sạch ở thư mục `evidence/` của Lab. Ẩn JWT, token, cookie và dữ liệu cá nhân.

## 7. Phân tích nguyên nhân

# Điểm kiểm soát bảo mật bị thiếu/sai:
- Endpoint 1: Response chứa object user với các trường email và number, trong khi chức năng tra cứu mechanic không yêu cầu những thông tin này.

- Endpoint 2: Danh sách bài viết chứa email và vehicleid của tác giả, bao gồm cả thông tin tác giả của các comments.

- Endpoint 3: Response chi tiết bài viết tiếp tục trả về email và vehicleid của tác giả và những người bình luận.

- Endpoint 4: Response sau thao tác bình luận chứa thông tin cá nhân của tác giả và người bình luận.

- Endpoint 5: Response cập nhật ảnh đại diện chứa available_credit, không cần thiết cho chức năng cập nhật ảnh.

- Endpoint 6: Response vị trí xe chứa fullName và email bên cạnh dữ liệu vị trí.

- Endpoint 7: Response danh sách xe chứa pincode, là thông tin cần được bảo vệ.

# Lớp cần khắc phục (API/Service/Database):
- API/Controller: Xác định các trường được phép xuất hiện trong response của từng endpoint.

- Service: Kiểm soát dữ liệu được lấy và xử lý trước khi trả về client.

- Serializer/DTO: Không tuần tự hóa toàn bộ object nếu chức năng chỉ cần một tập hợp trường giới hạn.

- Database: Chỉ truy vấn những thuộc tính cần thiết khi có thể, thay vì lấy toàn bộ dữ liệu không cần thiết.
# Phạm vi tác động đã chứng minh:
- Thông tin cá nhân: email, number, fullName.

- Thông tin liên quan đến phương tiện: vehicleid.

- Thông tin tài chính: available_credit.

- Thông tin bảo mật: pincode.

# Những điều chưa chứng minh:
- Khả năng sử dụng các trường dữ liệu bị lộ để thực hiện các hành vi chiếm quyền tài khoản hoặc gian lận tài chính.

- Nguyên nhân cụ thể trong mã nguồn backend do không thực hiện sửa đổi mã nguồn crAPI.

## 8. Biện pháp khắc phục

# Cách sửa được đề xuất:
- Sử dụng Serializer/DTO riêng cho từng endpoint:
-> Tránh sử dụng trực tiếp toàn bộ object từ database để tạo JSON response.

- Kiểm thử bảo mật định kỳ:
-> Duy trì các test case tự động để phát hiện những trường dữ liệu nhạy cảm xuất hiện trở lại trong response sau khi thay đổi hoặc mở rộng chức năng.

# Kiểm thử lại sau sửa:
1. Gửi lại các request đã lưu trong evidence.

2. Kiểm tra response mới của từng endpoint.

3. Đối chiếu các trường dữ liệu với mục đích nghiệp vụ.

4. Chạy lại toàn bộ test case bằng pytest.

5. Xác nhận những trường dữ liệu không cần thiết đã được loại bỏ.

6. Kiểm tra các chức năng nghiệp vụ vẫn hoạt động bình thường.

-> Kết quả mong đợi: không có phát hiện các trường dữ liệu thừa và gây rủi ro, mà vẫn đáp ứng đúng và đủ yêu cầu chức năng.

## 9. Automated security test

# File Python test: 
- test/security/test_data_exposure.py

# Tiền điều kiện:
- Chạy crAPI bằng file crapi.sh trong thư mục scripts

- Truy cập http://127.0.0.1:8888.

- Python virtual environment đã được kích hoạt.

- Tài khoản thử nghiệm được cấu hình thông qua biến môi trường hoặc giá trị mặc định trong test.

- Tài khoản có đủ dữ liệu để thực hiện các thao tác kiểm thử.

# Kết quả mong đợi trên vulnerable target:
- Dựa trên những response đã thu thập, kết quả phân loại dự kiến:

| Endpoint | Phát hiện | Mức độ |
|---|---|---|
| 1. Mechanic list | email, number | WARNING |
| 2. Recent posts | email, vehicleid | WARNING |
| 3. Post detail | email, vehicleid | WARNING |
| 4. Post comment | email, vehicleid | WARNING |
| 5. Upload picture | available_credit | FAILED |
| 6. Vehicle location | fullName, email | WARNING |
| 7. Vehicles list | pincode | FAILED |


# Kết quả thực tế:
- Chạy lệnh pytest -v tests/security/test_data_exposure.py
 
# Ý nghĩa PASS/FAIL/WARNING:
- PASS: Không phát hiện các trường dữ liệu thuộc danh sách kiểm tra trong response.

- WARNING: Phát hiện các trường dữ liệu có mức độ rủi ro thấp hoặc trung bình, chẳng hạn email, số điện thoại hoặc thông tin nhận dạng người dùng không cần thiết cho chức năng nghiệp vụ. Test được pytest ghi nhận là PASSED nhưng phát sinh UserWarning.

- FAILED: Phát hiện các trường dữ liệu có mức độ rủi ro cao, chẳng hạn thông tin xác thực hoặc thông tin tài chính quan trọng.


## 10. Kết luận và tham khảo

# Kết luận dựa trên bằng chứng:
- Qua quá trình thực nghiệm trên OWASP crAPI Challenge 4, đã khảo sát 7 API endpoints thông qua Burp Suite và phân tích các HTTP response tương ứng.

- Kết quả cho thấy các endpoints được kiểm tra có dấu hiệu Excessive Data Exposure khi trả về những trường dữ liệu không cần thiết đối với chức năng nghiệp vụ, bao gồm:
+ Thông tin cá nhân của người dùng: email, number và fullName.
+ Thông tin liên quan đến phương tiện: vehicleid.
+ Thông tin tài chính: available_credit.
+ Thông tin bảo mật: pincode.

# Tài liệu OWASP/API Security/nguồn chính thức:
1. OWASP API Security Top 10 – 2019: API3 Excessive Data Exposure.
2. OWASP crAPI – Challenge 4: Excessive Data Exposure.
