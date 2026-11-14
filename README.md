# ATTT-2026 — REST API Security Assessment & Hardening

Bài tập lớn An toàn thông tin: **nghiên cứu, khai thác và kiểm chứng các lỗ hổng REST API trên OWASP crAPI** theo OWASP API Security Top 10.

> **Chỉ sử dụng trong môi trường được phép.** crAPI cố tình có lỗ hổng. Nhóm chỉ kiểm thử các instance crAPI do chính nhóm triển khai trên máy cá nhân hoặc môi trường có ủy quyền. Không dùng công cụ quét vào website công khai.

## 1. Điều kiện chuẩn bị

- Git.
- Docker Engine/Desktop + Docker Compose V2.
- Python 3.11+ và pip.
- Burp Suite Community (nên có); OWASP ZAP (tùy bài kiểm thử).

**Lưu ý:** crAPI có nhiều microservices, có thể tốn RAM. Kiểm tra khả năng chạy từ ngày đầu; nếu máy yếu, thử cấu hình minimal do upstream cung cấp.

## 2. Khởi động crAPI

Repo nhóm **không sao chép hay chỉnh sửa Docker Compose của OWASP crAPI**. Script sẽ tải phiên bản chính thức vào thư mục cục bộ `.runtime/crapi/` (được gitignore) và chạy Compose của upstream.

~~~bash
bash scripts/crapi.sh setup    # Clone OWASP/crAPI (một lần)
bash scripts/crapi.sh up       # Docker Compose up -d
bash scripts/crapi.sh status   # Xem trạng thái containers
bash scripts/crapi.sh logs     # Xem log
bash scripts/crapi.sh down     # Dừng và loại bỏ containers/network
~~~

Mở ứng dụng: **http://127.0.0.1:8888**. Mail UI thử nghiệm (nếu dùng): **http://127.0.0.1:8025**.

Script cố định giao diện lắng nghe vào `127.0.0.1`. Lệnh `down` không yêu cầu xóa volumes. **Không dùng `down -v` nếu chưa thống nhất việc mất dữ liệu thử nghiệm.**

Lần chạy đầu cần Docker tải các image, có thể mất thời gian. Việc clone upstream chỉ chạy khi gọi `setup` hoặc `up` lần đầu; script **không tự cập nhật** lên commit mới. Ghi commit của crAPI trong tài liệu thực nghiệm để cả nhóm có cùng phiên bản.

**Nếu cần tự chạy thủ công:** Xem [tài liệu cài đặt crAPI chính thức](https://github.com/OWASP/crAPI/blob/main/docs/setup.md). Repo này không cố gắng thay thế hệ thống triển khai của upstream.

## 3. Chuẩn bị Python Security Tests

~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest -q
~~~

**Ban đầu:** 5 security test **được đánh dấu SKIPPED** vì chưa có logic kiểm thử. Đây chỉ là scaffold, **không phải** bộ kiểm thử đã phát hiện được lỗ hổng. Mỗi thành viên triển khai và bỏ dấu skip cho test của mình sau khi đã xác minh cách API hoạt động.

`tests/conftest.py` chỉ cho phép URL trỏ vào `localhost`/`127.0.0.1` để tránh kiểm thử nhầm hệ thống ngoài Lab.

## 4. Phạm vi 5 Lab

| Thành viên | Lab | Challenge crAPI | File test |
|---|---|---|---|
| TV1 | BOLA | #1 — Đọc thông tin phương tiện của người khác | `tests/security/test_bola.py` |
| TV2 | BFLA | #7 — Gọi chức năng xóa video vượt quyền | `tests/security/test_bfla.py` |
| TV3 | Excessive Data Exposure | #4 — Endpoint làm lộ thông tin nhạy cảm | `tests/security/test_data_exposure.py` |
| TV4 | Mass Assignment | #8 — Hoàn tiền cho món hàng chưa trả | `tests/security/test_mass_assignment.py` |
| TV5 | Unauthenticated Access | #14 — Endpoint thiếu kiểm tra xác thực | `tests/security/test_unauthenticated_access.py` |

Đây là các challenge được nêu trong [tài liệu crAPI](https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md). Chọn 5 Lab này nhằm bảo đảm từng người có một mảng nghiên cứu độc lập; thứ tự/khó khăn thực tế có thể thay đổi theo phiên bản upstream.

Mỗi người chỉ sửa thư mục `labs/0X-.../` và file `tests/security/test_...py` của mình. Mỗi người có **môi trường local**, bộ dữ liệu thử và tài khoản giả riêng để tránh xung đột.

## 5. Cấu trúc repository

~~~text
.
├── .github/                    # Issue/PR templates
├── docs/
│   ├── DE_TAI.md               # Phạm vi, mục tiêu
│   ├── ARCHITECTURE.md         # Kiến trúc thí nghiệm
│   ├── ROADMAP.md              # Lịch 7 ngày
│   ├── LAB_TEMPLATE.md         # Mẫu case study
│   └── SOURCES.md              # Nguồn tham khảo
├── labs/                       # 5 Lab độc lập
├── tests/
│   ├── conftest.py             # Fixture an toàn cho API client
│   └── security/               # 5 file Python test (scaffold)
├── scripts/
│   └── crapi.sh                # Chạy Docker Compose upstream
├── report/README.md           # Hướng dẫn tổng hợp báo cáo
├── presentation/README.md     # Hướng dẫn thuyết trình
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
~~~

## 6. Quy trình làm việc nhóm

1. Tạo GitHub repository **Private** và push bộ khung này.
2. Thêm 5 thành viên; chốt tên tương ứng TV1–TV5.
3. Mỗi người tạo branch `lab/bola`, `lab/bfla`, `lab/data-exposure`, `lab/mass-assignment`, `lab/unauthenticated-access`.
4. Tự thực nghiệm và viết báo cáo theo `docs/LAB_TEMPLATE.md`.
5. Khi có bằng chứng và test rõ ràng, mở Pull Request vào `main`; có ít nhất một thành viên review.
6. Tổng hợp báo cáo và slide sau khi các Lab bàn giao.

Đọc thêm [CONTRIBUTING.md](CONTRIBUTING.md).

## 7. Định nghĩa hoàn thành một Lab

- [ ] Có mô tả chức năng bình thường và điểm kiểm tra bảo mật.
- [ ] Tái hiện được lỗ hổng trên crAPI local; không chỉ sao chép lời giải.
- [ ] Có HTTP request/response được làm sạch thông tin nhạy cảm.
- [ ] Giải thích nguyên nhân, tác động và biện pháp phòng chống.
- [ ] Có ít nhất một security test thực thi được và kết quả thực tế được ghi nhận.
- [ ] Có hướng dẫn reset dữ liệu và demo trong tối đa 10 phút.
- [ ] Người khác review và xác nhận tính tái hiện.

## 8. Đưa lên GitHub

Sau khi giải nén repo và tạo repository trống trên GitHub:

~~~bash
git init -b main
git add .
git commit -m "chore: initialize crAPI security lab"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
~~~

Thay `USERNAME/REPO` bằng repository thực tế. Không push nếu chưa kiểm tra nội dung để tránh commit nhầm dữ liệu nhạy cảm.
