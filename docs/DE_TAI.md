# ATTT-2026 — Nội dung cần thực hiện

**Đề tài trong danh sách giảng viên:** Phân tích và khai thác lỗ hổng Web  
**Yêu cầu nhìn thấy từ ảnh:** “Sinh viên nghiên cứu và xây dựng lab minh họa kết quả.”  
**Phương án thực hiện:** Xây dựng Lab với OWASP Juice Shop, sử dụng Burp Suite và OWASP ZAP để phân tích, thực nghiệm và báo cáo ba lỗ hổng Web.

> Đây là phạm vi triển khai **đề xuất** dựa trên ảnh đề bài. Ảnh không quy định phải sử dụng tất cả công cụ, tự lập trình website hay khai thác bao nhiêu lỗ hổng. Cần xác nhận thêm nếu giảng viên có yêu cầu riêng.

## 1. Mục tiêu cần đạt

- [ ] Hiểu nguyên lý và tác động của các lỗ hổng Web được chọn.
- [ ] Xây dựng được môi trường Lab có thể chạy và thực hành trên máy cá nhân.
- [ ] Sử dụng công cụ để phân tích request, response và hành vi ứng dụng.
- [ ] Thực nghiệm, tái hiện và lưu bằng chứng của **3 lỗ hổng**.
- [ ] Giải thích nguyên nhân kỹ thuật và biện pháp phòng chống.
- [ ] Tổng hợp kết quả thành báo cáo và demo có thể thực hiện lại.

## 2. Phạm vi thực nghiệm

| Mã Lab | Loại lỗ hổng | Challenge trong OWASP Juice Shop | Kết quả cần chứng minh |
|---|---|---|---|
| LAB-01 | SQL Injection | **Login Admin** | Đầu vào không an toàn có thể ảnh hưởng việc xác thực |
| LAB-02 | Cross-Site Scripting (XSS) | **DOM XSS** | Dữ liệu không tin cậy có thể dẫn đến thực thi JavaScript ngoài ý muốn |
| LAB-03 | Broken Access Control | **View Basket** | Có thể truy cập giỏ hàng của tài khoản khác do kiểm tra quyền chưa đúng |

Ba challenge được xác nhận trong [OWASP Juice Shop Trainer’s Guide](https://pwning.owasp-juice.shop/companion-guide/latest/part4/trainers.html). Không mở rộng thêm challenge trước khi hoàn thành ba Lab chính.

**Công cụ dự kiến:**

- **OWASP Juice Shop:** Website được thiết kế cố ý có lỗ hổng để thực hành.
- **Docker:** Chạy Juice Shop trong môi trường riêng.
- **Burp Suite Community:** Quan sát, chặn và kiểm tra HTTP request/response.
- **OWASP ZAP:** Khảo sát bảo mật, thu thập cảnh báo để phân tích.
- **Browser DevTools:** Quan sát hành vi JavaScript và DOM, đặc biệt ở LAB-02.

## 3. Danh sách công việc cần làm

### A. Chuẩn bị môi trường Lab

- [ ] Cài đặt và kiểm tra Docker hoạt động.
- [ ] Tải và khởi chạy OWASP Juice Shop trên localhost.
- [ ] Truy cập được giao diện ứng dụng tại http://localhost:3000.
- [ ] Cài đặt Burp Suite Community và OWASP ZAP.
- [ ] Cấu hình trình duyệt/proxy và thử quan sát một HTTP request bằng Burp.
- [ ] Ghi lại phiên bản công cụ, Docker image và các bước khởi động để tái hiện.
- [ ] Tạo các tài khoản thử nghiệm giả lập cần thiết, đặc biệt hai tài khoản riêng cho LAB-03.

Có thể khởi động Juice Shop bằng:

~~~bash
docker pull bkimminich/juice-shop
docker run --rm --name attt-juice-shop -p 127.0.0.1:3000:3000 bkimminich/juice-shop
~~~

Chỉ sử dụng các tài khoản và dữ liệu giả trong môi trường Lab. Không mở cổng Lab ra Internet.

### B. Nghiên cứu kiến thức nền

- [ ] Tìm hiểu cách HTTP request/response và session đăng nhập hoạt động.
- [ ] Tìm hiểu khái niệm, nguyên nhân và tác động của SQL Injection.
- [ ] Tìm hiểu DOM-based XSS và cách dữ liệu được xử lý trên trình duyệt.
- [ ] Tìm hiểu Broken Access Control, phân biệt **authentication** và **authorization**.
- [ ] Nghiên cứu cách phòng chống tương ứng với từng loại lỗ hổng.

### C. Thực nghiệm LAB-01 — SQL Injection

- [ ] Khảo sát chức năng đăng nhập thông thường.
- [ ] Ghi nhận các request/response liên quan bằng Burp Suite.
- [ ] Tái hiện challenge **Login Admin** trên Juice Shop local.
- [ ] Chụp bằng chứng trước và sau thử nghiệm; lưu trạng thái challenge nếu có.
- [ ] Giải thích nguyên nhân ở cơ chế tạo/thực thi câu truy vấn.
- [ ] Nêu tác động, biện pháp phòng chống bằng **parameterized query/prepared statement** và test case kiểm chứng.

### D. Thực nghiệm LAB-02 — DOM XSS

- [ ] Khảo sát chức năng liên quan đến dữ liệu đầu vào trên trang web.
- [ ] Dùng Browser DevTools xác định đường đi dữ liệu trong DOM.
- [ ] Tái hiện challenge **DOM XSS** trên Juice Shop local.
- [ ] Lưu bằng chứng hành vi trình duyệt và trạng thái challenge nếu có.
- [ ] Giải thích dữ liệu đi từ **source** đến **sink** không an toàn như thế nào.
- [ ] Đề xuất sử dụng DOM API an toàn, xử lý đầu ra theo ngữ cảnh và các biện pháp bổ sung phù hợp.

### E. Thực nghiệm LAB-03 — Broken Access Control

- [ ] Tạo hai tài khoản thử nghiệm A và B; chuẩn bị hai giỏ hàng có dữ liệu phân biệt.
- [ ] Quan sát request khi mỗi tài khoản truy cập giỏ hàng của mình.
- [ ] Tái hiện challenge **View Basket** trong Lab.
- [ ] Lưu bằng chứng cho thấy quyền truy cập không phù hợp giữa hai tài khoản.
- [ ] Giải thích nguyên nhân thiếu kiểm tra quyền trên tài nguyên ở phía server.
- [ ] Đề xuất kiểm tra quyền sở hữu tài nguyên và test case từ chối truy cập trái phép.

### F. Kiểm thử bổ sung bằng OWASP ZAP

- [ ] Chỉ định phạm vi quét là instance Juice Shop được phép kiểm thử.
- [ ] Thu thập request và kết quả **passive scan**.
- [ ] Chạy **active scan** chỉ khi target là Lab cục bộ và đã chuẩn bị cho việc dữ liệu thử nghiệm có thể thay đổi.
- [ ] Xuất báo cáo/ảnh chụp các cảnh báo.
- [ ] Kiểm chứng thủ công những cảnh báo được đưa vào báo cáo.
- [ ] Nêu rõ trường hợp công cụ không phát hiện hoặc phát hiện chưa chính xác.

> Kết quả scan tự động không tự động chứng minh đã khai thác thành công; đặc biệt DOM XSS và lỗi phân quyền cần kiểm thử thủ công.

### G. Phân tích và tổng hợp kết quả

- [ ] Mô tả cách tái hiện từng lỗ hổng bằng những bước rõ ràng.
- [ ] Phân tích nguyên nhân kỹ thuật và tác động của từng lỗ hổng.
- [ ] Trình bày biện pháp phòng chống và cách kiểm thử sau khi khắc phục.
- [ ] Đối chiếu kết quả kiểm thử thủ công với cảnh báo từ ZAP (nếu có).
- [ ] Ghi lại giới hạn thực nghiệm và những điều chưa chứng minh được.
- [ ] Kiểm tra hình ảnh, trích dẫn nguồn và tính nhất quán của kết luận.

## 4. Bằng chứng cần lưu cho mỗi Lab

| Loại bằng chứng | Nội dung |
|---|---|
| Trạng thái ban đầu | Giao diện/hành vi hợp lệ trước thực nghiệm |
| Các bước tái hiện | Hướng dẫn đủ rõ để thực hiện lại |
| Request/response hoặc DevTools | Dữ liệu kỹ thuật có liên quan, đã ẩn cookie/token |
| Kết quả | Ảnh hoặc bản ghi hành vi bất thường, Score Board nếu phù hợp |
| Giải thích | Nguyên nhân, tác động, biện pháp phòng chống |
| Kiểm thử sau sửa | Kịch bản kiểm tra cách hệ thống nên từ chối/xử lý an toàn |

## 5. Sản phẩm cần hoàn thành

- [ ] **Lab hoạt động:** Juice Shop chạy được bằng Docker, có hướng dẫn khởi động.
- [ ] **3 case study:** SQL Injection, DOM XSS, Broken Access Control.
- [ ] **Bộ bằng chứng:** Ảnh, log hoặc request/response được làm sạch, có chú thích.
- [ ] **Kết quả OWASP ZAP:** Báo cáo quét và phần phân tích, có xác minh khi cần.
- [ ] **Báo cáo bài tập lớn:** Giới thiệu, mục tiêu, lý thuyết, kiến trúc Lab, phương pháp, 3 case study, kết quả và kết luận.
- [ ] **Slide thuyết trình:** Trình bày ngắn gọn mục tiêu, môi trường, 3 demo và bài học.
- [ ] **Kịch bản demo:** Chuẩn bị các bước thực hiện lại và ảnh/video dự phòng nếu demo trực tiếp gặp lỗi.

## 6. Điều kiện coi là hoàn thành

- [ ] Môi trường Lab chạy ổn định trên ít nhất một máy.
- [ ] Cả ba Lab có bằng chứng thực nghiệm rõ ràng, trung thực.
- [ ] Mỗi lỗ hổng đều nêu được **nguyên nhân → tác động → phòng chống**.
- [ ] Kết quả từ ZAP được diễn giải đúng, không coi cảnh báo là bằng chứng khai thác khi chưa kiểm chứng.
- [ ] Báo cáo và slide khớp với kết quả thực tế.
- [ ] Có thể trình diễn hoặc tái hiện các bước chính trong buổi bảo vệ.

## 7. Những điểm cần xác nhận với giảng viên

- [ ] Có bắt buộc tự viết website hay được sử dụng Juice Shop có sẵn?
- [ ] Có bắt buộc sử dụng tất cả công cụ trong danh sách đề bài?
- [ ] Có yêu cầu số lượng lỗ hổng tối thiểu hoặc bản vá chạy được?
- [ ] Có mẫu báo cáo và thời lượng demo/bảo vệ cụ thể không?

## 8. Tài liệu tham khảo

1. [OWASP — Juice Shop](https://devguide.owasp.org/en/07-training-education/01-vulnerable-apps/01-juice-shop/)
2. [OWASP Juice Shop — Companion Guide](https://pwning.owasp-juice.shop/companion-guide/latest/)
3. [OWASP Juice Shop — Trainer’s Guide](https://pwning.owasp-juice.shop/companion-guide/latest/part4/trainers.html)
4. [OWASP ZAP — Getting Started](https://www.zaproxy.org/getting-started/)

**Nguyên tắc:** Chỉ thực hiện kiểm thử trên môi trường Lab do nhóm quản lý hoặc mục tiêu có ủy quyền rõ ràng.
