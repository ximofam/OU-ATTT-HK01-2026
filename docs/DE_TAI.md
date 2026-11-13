# Đề tài — Phân tích và khai thác lỗ hổng Web

## Nội dung đề bài quan sát được

- **Tên:** Phân tích và khai thác lỗ hổng Web.
- **Yêu cầu:** Sinh viên nghiên cứu và xây dựng Lab minh họa kết quả.
- **Công cụ được gợi ý:** Burp Suite, OWASP ZAP, Nikto, Wapiti, Retire.js... và ứng dụng có lỗ hổng chạy container (WebGoat, Juice Shop).

Đề bài nhìn thấy **không yêu cầu rõ** phải lập trình website, phải dùng toàn bộ công cụ hay phải thực hiện bao nhiêu lỗ hổng. Cần xác nhận lại nếu giảng viên bổ sung yêu cầu.

## Công việc nhóm cần làm

1. Triển khai OWASP Juice Shop bằng Docker Compose trên localhost.
2. Nghiên cứu nguyên lý, nguyên nhân và tác động của từng lỗ hổng được chọn.
3. Sử dụng Burp Suite, OWASP ZAP hoặc Browser DevTools phù hợp để khảo sát.
4. Thực nghiệm các challenge trong môi trường được phép.
5. Ghi lại các điều kiện ban đầu, các bước tái hiện và bằng chứng kiểm thử.
6. Giải thích vì sao ứng dụng có lỗ hổng và biện pháp phòng chống.
7. Chuẩn bị báo cáo, slide và demo chạy lại kết quả.

## Phạm vi thực nghiệm đề xuất

| Loại | Challenge | Trạng thái phạm vi |
|---|---|---|
| SQL Injection | Login Admin | Chính |
| DOM XSS | DOM XSS | Chính |
| Broken Access Control | View Basket | Chính |
| Sensitive Data Exposure | Confidential Document | **Đề xuất bổ sung, cần chốt** |

## Kết quả bàn giao

- Hướng dẫn khởi động Lab (`README.md`, `compose.yaml`).
- Một tài liệu và bộ bằng chứng cho mỗi Lab.
- Báo cáo tổng hợp, kết quả công cụ quét nếu có và tài liệu tham khảo.
- Slide và kịch bản trình diễn có thể lặp lại.

**Nguyên tắc:** Chỉ thử nghiệm trên Lab của nhóm hoặc mục tiêu có ủy quyền; không khai thác hệ thống của người khác.
