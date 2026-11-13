# LAB-04 — Sensitive Data Exposure (đề xuất bổ sung)

**Challenge:** Confidential Document (OWASP Juice Shop)  
**Công cụ chính:** Trình duyệt, OWASP ZAP.

> Lab này **chưa nằm trong bộ 3 Lab chính ban đầu**. Nhóm cần chốt có đưa vào phạm vi chính thức không.

## Cần thực hiện

- [ ] Nghiên cứu nguyên nhân tài liệu nhạy cảm bị truy cập không đúng quyền.
- [ ] Khởi động Juice Shop local.
- [ ] Khảo sát đường dẫn và các tài nguyên được công bố trên website.
- [ ] Tái hiện challenge Confidential Document trong Lab.
- [ ] Chạy OWASP ZAP Passive Scan trên **chính instance local được phép**.
- [ ] Lưu bằng chứng và phân biệt kết quả thủ công với cảnh báo tự động tại `evidence/`.
- [ ] Đề xuất kiểm soát truy cập, cấu hình tài nguyên và giới hạn công khai file.
- [ ] Viết tài liệu theo `docs/LAB_TEMPLATE.md`.

## Đầu ra

Một báo cáo độc lập, bằng chứng thực nghiệm và nhận xét ZAP. Không khẳng định ZAP phải tự phát hiện challenge này.
