# LAB-03 — Excessive Data Exposure

## 1. Mục tiêu và phạm vi

- OWASP API Security category: API3 - Excessive Data Exposure.

- crAPI challenge: Challenge 4 - Tìm các endpoints API làm lộ thông tin nhạy cảm của người dùng.

- Tác động cần kiểm chứng:

+ API trả về các trường dữ liệu nhạy cảm không cần thiết cho chức năng nghiệp vụ.
+ Người dùng hiện tại có thể nhận được thông tin thuộc tài khoản khác.
+ Các thông tin nhạy cảm bị thu thập thông qua các endpoints mà không cần vượt qua cơ chế xác thực.

## 2. Lý thuyết

- Khái niệm: tình trạng API trả về dữ liệu hơn mức cần thiết cho chức năng nghiệp, làm lộ các thông tin nhạy cảm và ảnh hưởng đến quyền riêng tư của người dùng.

- Nguyên nhân thường gặp:

+ API trả về toàn bộ thông tin của đối tượng:
Backend truy vấn một đối tượng trong database và tuần tự hóa toàn bộ thuộc tính thành JSON response, thay vì chỉ trả về những trường cần thiết.

+ Serializer hoặc DTO chứa quá nhiều trường:
Lập trình viên đưa nhiều thuộc tính vào serializer hoặc DTO mà không đánh giá mức độ cần thiết của từng trường đối với chức năng nghiệp vụ.

+ Chỉ ẩn dữ liệu ở phía frontend:
Frontend chỉ hiển thị một số trường nhất định nhưng backend vẫn gửi toàn bộ dữ liệu trong response.

+ Thiếu kiểm soát quyền truy cập ở cấp thuộc tính:
Backend không phân biệt trường dữ liệu nào được phép trả về cho từng loại người dùng hoặc từng chức năng nghiệp vụ.

- Biện pháp phòng chống:

+ Data Minimization:
Chỉ trả về những trường dữ liệu thực sự cần thiết cho chức năng nghiệp vụ.

+ Data Minimization:
Chỉ trả về những trường dữ liệu thực sự cần thiết cho chức năng nghiệp vụ.

+ Kiểm soát quyền truy cập ở cấp thuộc tính:
Xác định người dùng hoặc vai trò nào được phép truy cập từng trường dữ liệu.

- Các nhóm thông tin nhạy cảm:
Nhóm 1: Thông tin xác thực và bảo mật
+ password
+ password_hash
+ access_token
+ refresh_token
+ reset_token
+ secret_key
+ api_key
+ private_key

Nhóm 2: Thông tin dạng cá nhân (Personally Identifiable Information - PII)
+ email
+ phone
+ address
+ date_of_birth
+ full_name
+ national_id
+ passport_number
+ location

Nhóm 3: Thông tin tài chính
+ credit_card_number
+ bank_account
+ balance
+ transaction_history
+ payment_details
+ billing_address

Nhóm 4: Thông tin nội bộ và nghiệp vụ
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

- Môi trường: OWASP crAPI

- Triển khai: chạy môi trường local với Docker:
+ crAPI: 127.0.0.1:8888 (với listener chạy với port: 8081)
+ mailHog: 127.0.0.1:8025
+ firefox: 127.0.0.1:8081

- Công cụ: Burpsuite

- Tài khoản thử nghiệm/điều kiện ban đầu (không ghi credentials):
+ Tài khoản 1: Tên người dùng: truong, Email: truong123@gmail



## 4. Khảo sát chức năng bình thường

- Mục đích nghiệp vụ của API:

+ Endpoint 1:

+ Endpoint 2:

+ Endpoint 3:

+ Endpoint 4:

+ Endpoint 5:

+ Endpoint 6:

+ Endpoint 7:

- Endpoint và method liên quan:

+ Endpoint 1:
Method: GET
Path: /workshop/api/mechanic

+ Endpoint 2:
Method: GET
Path: /community/api/v2/community/posts/recent

+ Endpoint 3:
Method: GET
Path: /community/api/v2/community/posts/{id}

+ Endpoint 4:
Method: POST
Path: /community/api/v2/community/posts/{id}/comment

+ Endpoint 5:
Method: POST
Path: /identity/api/v2/user/pictures

+ Endpoint 6:
Method: GET
Path: /identity/api/v2/vehicle/{id}/location

+ Endpoint 7:
Method: GET
Path: /identity/api/v2/vehicle/vehicles

- Request/response hợp lệ:

+ Endpoint 1:

+ Endpoint 2:

+ Endpoint 3:

+ Endpoint 4:

+ Endpoint 5:

+ Endpoint 6:

+ Endpoint 7:


## 5. Phương pháp kiểm thử

1. Các bước khởi tạo dữ liệu.
2. Các bước kiểm thử có kiểm soát trong Lab.
3. Dấu hiệu để xác nhận hành vi sai quyền/bất thường.
4. Cách chạy lại bằng test Python.

## 6. Bằng chứng

Đặt ảnh và request/response đã làm sạch ở thư mục `evidence/` của Lab. Ẩn JWT, token, cookie và dữ liệu cá nhân.

## 7. Phân tích nguyên nhân

- Điểm kiểm soát bảo mật bị thiếu/sai:
- Lớp cần khắc phục (API/Service/Database):
- Phạm vi tác động đã chứng minh:
- Những điều chưa chứng minh:

## 8. Biện pháp khắc phục

- Cách sửa được đề xuất:
- Kiểm thử lại sau sửa:

## 9. Automated security test

- File Python test:
- Tiền điều kiện:
- Kết quả mong đợi trên vulnerable target:
- Kết quả thực tế:
- Ý nghĩa PASS/FAIL/SKIP:

## 10. Kết luận và tham khảo

- Kết luận dựa trên bằng chứng:
- Tài liệu OWASP/API Security/nguồn chính thức:
