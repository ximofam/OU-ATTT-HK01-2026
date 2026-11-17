# Bằng chứng — Luồng nghiệp vụ hợp lệ

Môi trường: crAPI 1.1.5 (commit `700f03d`), `http://127.0.0.1:8888`.
Token JWT và email tài khoản thử đã được che.

## 1. Đăng ký tài khoản thử

```http
POST /identity/api/auth/signup HTTP/1.1
Content-Type: application/json

{"name":"Vien Lab04","email":"<test-account>@example.com","number":"<test-phone>","password":"<redacted>"}
```

```http
HTTP/1.1 200 OK

{"message":"User registered successfully! Please Login.","status":200}
```

## 2. Đăng nhập

```http
POST /identity/api/auth/login HTTP/1.1
Content-Type: application/json

{"email":"<test-account>@example.com","password":"<redacted>"}
```

```http
HTTP/1.1 200 OK

{"token":"<JWT redacted>","type":"Bearer","message":"","isMfaRequired":false}
```

## 3. Số dư và danh sách sản phẩm ban đầu

```http
GET /workshop/api/shop/products?offset=0&limit=10 HTTP/1.1
Authorization: Bearer <JWT redacted>
```

```http
HTTP/1.1 200 OK

{"products":[{"id":2,"name":"Wheel","price":"10.00"},{"id":1,"name":"Seat","price":"10.00"}],"credit":100.0}
```

## 4. Mua 1 sản phẩm — credit giảm đúng 10

```http
POST /workshop/api/shop/orders HTTP/1.1
Authorization: Bearer <JWT redacted>
Content-Type: application/json

{"product_id":1,"quantity":1}
```

```http
HTTP/1.1 200 OK

{"id":6,"message":"Order sent successfully.","credit":90.0}
```

## 5. Hoàn hàng hợp lệ — tạo QR, chuyển trạng thái sang `return pending`

```http
POST /workshop/api/shop/orders/return_order?order_id=6 HTTP/1.1
Authorization: Bearer <JWT redacted>
```

```http
HTTP/1.1 200 OK

{"message":"Please use the following QR code to return your order to a UPS store!",
 "qr_code_url":"http://127.0.0.1:8888/workshop/api/shop/return_qr_code",
 "order":{"id":6,"quantity":1,"status":"return pending"}}
```

Kết luận: luồng hợp lệ chỉ hoàn tiền sau khi người dùng thực sự mang hàng đến UPS và
trạng thái đơn được cập nhật bởi quy trình của cửa hàng.
