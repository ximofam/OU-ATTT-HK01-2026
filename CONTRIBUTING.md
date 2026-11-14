# Làm việc nhóm và Pull Request

## Chiến lược branch

| Branch | Phạm vi |
|---|---|
| `lab/bola` | `labs/01-bola/`, `tests/security/test_bola.py` |
| `lab/bfla` | `labs/02-bfla/`, `tests/security/test_bfla.py` |
| `lab/data-exposure` | `labs/03-data-exposure/`, `tests/security/test_data_exposure.py` |
| `lab/mass-assignment` | `labs/04-mass-assignment/`, `tests/security/test_mass_assignment.py` |
| `lab/unauthenticated-access` | `labs/05-unauthenticated-access/`, `tests/security/test_unauthenticated_access.py` |

Không chỉnh sửa chung fixture, script khởi động hoặc docs tổng hợp nếu chưa thống nhất trong nhóm. Mỗi người có thể chạy một instance crAPI local riêng.

## PR checklist

- [ ] Đã triển khai ít nhất một security test (không còn SKIPPED cho case đã hoàn thành).
- [ ] Có bằng chứng thật, đã che token/session/cookie.
- [ ] Có hướng dẫn tạo tài khoản/seed dữ liệu để chạy lại.
- [ ] Có phân tích nguyên nhân, tác động, mitigation.
- [ ] Không commit dữ liệu thật, Burp project, HAR chưa được làm sạch.
- [ ] Đã có review chéo trước khi merge.

## Giải thích kỳ vọng test

- CrAPI intentionally vulnerable: một security regression test kiểm tra **hành vi an toàn** có thể **FAIL** trên crAPI. Đây có thể chính là bằng chứng lỗ hổng.
- Test FAIL phải có mô tả/tái hiện rõ ràng; không biến một lỗi mạng hoặc setup thành “phát hiện bảo mật”.
- Chỉ nói test **PASS sau khi vá** khi có phiên bản thực sự đã khắc phục và đã chạy kiểm chứng.

Không cấu hình workflow bắt buộc tất cả security tests PASS trên bản crAPI vốn cố tình có lỗ hổng.
