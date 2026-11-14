# Đề cương — REST API Security Assessment & Hardening

**Tên tiếng Việt:** Nghiên cứu, phân tích, khai thác và tăng cường bảo mật REST API theo OWASP API Security Top 10.  
**Tên tiếng Anh:** REST API Security Assessment and Hardening Based on OWASP API Security Top 10.  
**Phạm vi nhóm:** 5 thành viên, thời gian thực hiện 7 ngày.

## 1. Liên hệ đề tài được giao

Đề tài giảng viên cung cấp trong ảnh: **Phân tích và khai thác lỗ hổng Web**, yêu cầu nghiên cứu và xây dựng Lab minh họa kết quả. API Security là một hướng triển khai chuyên sâu của đề tài này. Nếu giảng viên yêu cầu giữ nguyên tên hoặc danh mục công cụ, nhóm cần xác nhận lại trước khi nộp tên mới.

## 2. Mục tiêu

1. Triển khai một môi trường API có lỗ hổng phục vụ kiểm thử được cho phép.
2. Xây dựng và thực hiện kịch bản kiểm thử thủ công cho 5 loại lỗ hổng.
3. Viết các bài kiểm thử bảo mật tự động bằng Python/Pytest.
4. Phân tích cơ chế lỗi, tác động và biện pháp phòng chống.
5. Có bằng chứng thực nghiệm có thể tái hiện và báo cáo rõ ràng.
6. Nếu còn thời gian, chứng minh bản vá minh họa và kết quả kiểm thử hồi quy.

## 3. Đối tượng thực nghiệm

**OWASP crAPI**, một ứng dụng Web API dựa trên microservices cố tình chứa lỗ hổng. Nhóm sử dụng các challenge chính thức làm đầu vào nghiên cứu; sản phẩm tự xây là bộ kiểm thử, phương pháp phân tích và báo cáo. Việc chạy crAPI không được xem là sản phẩm lập trình của nhóm.

## 4. Phạm vi 5 Lab

| Mã | Loại lỗ hổng | Challenge crAPI | Mục tiêu nghiên cứu |
|---|---|---|---|
| LAB-01 | BOLA | #1 — Another user's vehicle | Kiểm soát quyền trên từng object |
| LAB-02 | BFLA | #7 — Delete another user's video | Kiểm soát quyền theo chức năng |
| LAB-03 | Excessive Data Exposure | #4 — Sensitive info exposure | Giới hạn dữ liệu trả về |
| LAB-04 | Mass Assignment | #8 — Invalid refund | Bảo vệ thuộc tính/luồng nghiệp vụ |
| LAB-05 | Unauthenticated Access | #14 — Missing authentication | Bắt buộc xác thực tại API phù hợp |

Chi tiết danh sách challenge: [OWASP crAPI — Challenges](https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md).

## 5. Công việc cần thực hiện

- [ ] Triển khai crAPI bằng Docker Compose chính thức, kiểm tra môi trường chạy ổn định.
- [ ] Nghiên cứu API Security Top 10 và các nhóm lỗi được giao.
- [ ] Khảo sát request/response, endpoint, account và workflow có liên quan.
- [ ] Viết kịch bản khai thác trong Lab; ghi lại kết quả và bằng chứng.
- [ ] Viết 5 file automated security tests; kiểm chứng được các hành vi mục tiêu.
- [ ] Phân tích và xác minh lỗi; không nhầm sự cố môi trường với lỗ hổng.
- [ ] Đề xuất giải pháp khắc phục và test case sau sửa.
- [ ] Hoàn thiện báo cáo, slide và kịch bản demo.

## 6. Sản phẩm cần nộp

1. Repository chứa tài liệu và mã kiểm thử.
2. Hướng dẫn triển khai crAPI bằng Docker Compose.
3. 5 báo cáo thực nghiệm độc lập, có bằng chứng đã làm sạch thông tin nhạy cảm.
4. Bộ automated security tests thực thi được trên Lab.
5. Báo cáo tổng hợp và slide.
6. Phần sửa lỗi minh họa và regression tests nếu kịp tiến độ.

## 7. Giới hạn và an toàn

- Không tự xây lại crAPI, không phát triển scanner toàn diện.
- Không cam kết vá trực tiếp mọi lỗi trong crAPI; đây là ứng dụng cố tình có lỗ hổng.
- Không chạy test trên API ngoài môi trường được cho phép.
- Không commit cookie, JWT, mật khẩu thật, file HAR hoặc log chứa credentials.
- Không đánh đồng kết quả scanner với kết quả được xác minh thủ công.

## 8. Những điều cần hỏi giảng viên

- [ ] Có chấp nhận chuyển trọng tâm từ Web UI sang REST API Security không?
- [ ] Có bắt buộc tự lập trình ứng dụng mục tiêu không?
- [ ] Có yêu cầu báo cáo/slide hoặc số lượng lỗ hổng tối thiểu không?
- [ ] Có yêu cầu sửa lỗi thật trong source code thay vì phương án sửa minh họa không?
