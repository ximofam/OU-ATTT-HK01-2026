# ATTT-2026 — Web Vulnerability Analysis Lab

Bài tập lớn môn **An toàn thông tin**: nghiên cứu, phân tích và thực nghiệm các lỗ hổng bảo mật Web trên **OWASP Juice Shop** trong Docker.

> **Chỉ sử dụng trong môi trường học tập được phép.** Juice Shop là ứng dụng cố ý có lỗ hổng. Compose chỉ mở cổng tại `127.0.0.1`; không triển khai công khai lên Internet.

## 1. Điều kiện chuẩn bị

- Docker Engine hoặc Docker Desktop.
- Docker Compose V2 (lệnh `docker compose`).
- Một trình duyệt hiện đại.
- Burp Suite Community, OWASP ZAP nếu cần theo bài thực nghiệm.

**Lưu ý:** Docker Compose **không bắt buộc** để chạy Juice Shop, nhưng giúp mọi thành viên dùng chung một cấu hình và dễ chạy lại Lab.

## 2. Chạy Lab

Từ thư mục gốc repo:

~~~bash
docker compose pull
docker compose up -d
docker compose ps
~~~

Truy cập: **http://localhost:3000**.

Xem log:

~~~bash
docker compose logs -f juice-shop
~~~

Dừng và loại bỏ container cùng network do Compose tạo:

~~~bash
docker compose down
~~~

Lab dùng dữ liệu thử nghiệm. Không định nghĩa persistent volume; khi container bị xóa, trạng thái thử nghiệm trong container có thể bị mất. Mỗi Lab cần có hướng dẫn thiết lập lại dữ liệu để tái hiện từ đầu.

**Tính tái lập:** File dùng image tag `latest` để dễ bắt đầu. Trước ngày nộp, cả nhóm nên thống nhất và cố định cùng **tag hoặc digest** đã chạy thành công; ghi vào báo cáo. Không cập nhật image giữa các buổi tổng duyệt.

## 3. Cấu trúc repository

~~~text
.
├── compose.yaml                      # Khởi động OWASP Juice Shop
├── README.md                         # Hướng dẫn chung
├── .gitignore                        # Tránh commit secrets/tool logs
├── .github/
│   ├── ISSUE_TEMPLATE/lab-task.md    # Mẫu issue cho mỗi Lab
│   └── pull_request_template.md      # Checklist khi nộp PR
├── docs/
│   ├── DE_TAI.md                     # Phạm vi và mục tiêu
│   ├── LAB_TEMPLATE.md               # Form báo cáo dùng chung
│   └── SOURCES.md                    # Tài liệu chính thức
├── labs/
│   ├── 01-sql-injection/
│   ├── 02-dom-xss/
│   ├── 03-broken-access-control/
│   └── 04-sensitive-data-exposure/   # Phương án thêm Lab độc lập
├── report/README.md                  # Hướng dẫn tổng hợp báo cáo
└── presentation/README.md            # Hướng dẫn slide và demo
~~~

## 4. Phạm vi Lab

| Thư mục | Challenge Juice Shop | Nội dung |
|---|---|---|
| `labs/01-sql-injection` | Login Admin | SQL Injection |
| `labs/02-dom-xss` | DOM XSS | Cross-Site Scripting |
| `labs/03-broken-access-control` | View Basket | Truy cập trái quyền |
| `labs/04-sensitive-data-exposure` | Confidential Document | Lộ tài liệu nhạy cảm |

**Ba Lab đầu** là phạm vi đã ghi trong tài liệu đề tài trước đó; **Lab 04** là phương án mở rộng để nhóm có bốn phần độc lập, cần được nhóm chốt trước khi nộp đề cương.

Mỗi Lab có thể làm hoàn toàn độc lập bằng **một Juice Shop local riêng**. Không cần tự viết frontend/backend mới. Mỗi Lab phải có lý thuyết, phương pháp, bằng chứng, tác động và đề xuất khắc phục.

## 5. Quy trình cộng tác trên GitHub

1. Tạo **GitHub repository riêng tư** cho nhóm, upload toàn bộ cấu trúc này.
2. Thêm cả bốn thành viên vào repository.
3. Mỗi người tạo issue cho Lab của mình bằng mẫu `.github/ISSUE_TEMPLATE/lab-task.md`.
4. Tạo một branch độc lập, ví dụ: `lab/sql-injection`, `lab/dom-xss`, `lab/access-control`, `lab/sensitive-data`.
5. Mỗi thành viên **chỉ sửa thư mục Lab của mình**, hạn chế conflict khi làm song song.
6. Khi hoàn thành, tạo Pull Request vào `main` và nhờ ít nhất một người review.
7. Các tài liệu chung (`docs/`, `report/`, `presentation/`) được tổng hợp sau khi các Lab có bằng chứng hoàn chỉnh.

Không commit thông tin đăng nhập thật, JWT, session cookie, Burp project hoặc HAR chứa dữ liệu chưa được ẩn. Ảnh minh họa cũng cần được kiểm tra trước khi đưa lên GitHub.

## 6. Điều kiện hoàn thành một Lab

- [ ] Có hướng dẫn setup và các dữ liệu/điều kiện ban đầu.
- [ ] Có kịch bản tái hiện từ đầu.
- [ ] Có ảnh, request/response hoặc DevTools evidence thực tế đã làm sạch.
- [ ] Giải thích được nguyên nhân và tác động bảo mật.
- [ ] Có giải pháp phòng chống và test case kiểm tra lại.
- [ ] Thành viên khác có thể tái hiện trong tối đa 10 phút theo tài liệu.

## 7. Lệnh thường dùng

~~~bash
docker compose up -d             # Khởi động
docker compose ps                # Xem trạng thái
docker compose logs juice-shop   # Xem log
docker compose down              # Dừng và loại bỏ container
~~~

**Không chạy Active Scan vào website ngoài phạm vi Lab đã được cấp quyền.**
