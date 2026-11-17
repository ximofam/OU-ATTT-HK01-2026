"""LAB-03: Excessive Data Exposure — sensitive information in API responses."""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urlparse

import pytest
import requests

# Ảnh PNG 1x1 pixel hợp lệ (67 bytes) dùng để test upload avatar mà không cần file ngoài
MINIMAL_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

# Các nhóm trường nhạy cảm không được phép xuất hiện trong response
PII_FIELDS = {"email", "phone", "number", "fullName", "fullname", "vehicleid", "vehicleId"}
FINANCIAL_FIELDS = {"available_credit", "availableCredit", "credit"}
AUTH_FIELDS = {"pincode", "pin_code", "password", "token", "secret"}


class CrAPIClientAdapter:
    """Wrapper chuẩn hóa cách gọi HTTP bất kể fixture api_client trong conftest.py cài đặt ra sao."""

    def __init__(self, api_client: Any) -> None:
        self.raw_client = api_client
        self.base_url = self._resolve_base_url(api_client)
        self._validate_local_target(self.base_url)
        self.session = requests.Session()
        self.token: str | None = None

    @staticmethod
    def _resolve_base_url(api_client: Any) -> str:
        for attr in ("base_url", "url", "host"):
            val = getattr(api_client, attr, None)
            if isinstance(val, str) and val.startswith("http"):
                return val.rstrip("/")
        return os.getenv("CRAPI_BASE_URL", "http://127.0.0.1:8888").rstrip("/")

    @staticmethod
    def _validate_local_target(base_url: str) -> None:
        parsed = urlparse(base_url)
        if parsed.hostname not in {"127.0.0.1", "localhost"}:
            pytest.fail(
                f"Chỉ được phép chạy security test trên môi trường local (127.0.0.1/localhost), "
                f"nhưng nhận được: {base_url}"
            )

    def _build_url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if extra:
            headers.update(extra)
        return headers

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        headers = self._headers(kwargs.pop("headers", None))
        return self.session.get(self._build_url(path), headers=headers, timeout=15, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        headers = self._headers(kwargs.pop("headers", None))
        return self.session.post(self._build_url(path), headers=headers, timeout=15, **kwargs)

    def authenticate(self, email: str, password: str, name: str, number: str) -> None:
        """Đăng nhập tài khoản thử nghiệm; tự động đăng ký nếu tài khoản chưa tồn tại."""
        login_payload = {"email": email, "password": password}
        try:
            resp = self.post("/identity/api/auth/login", json=login_payload)
        except requests.RequestException as exc:
            pytest.fail(f"Không thể kết nối tới crAPI tại {self.base_url}: {exc}")

        if resp.status_code != 200:
            signup_payload = {
                "name": name,
                "email": email,
                "number": number,
                "password": password,
            }
            signup_resp = self.post("/identity/api/auth/signup", json=signup_payload)
            if signup_resp.status_code not in {200, 201}:
                pytest.fail(
                    f"Không thể tạo tài khoản thử nghiệm ({signup_resp.status_code}): {signup_resp.text}"
                )
            resp = self.post("/identity/api/auth/login", json=login_payload)

        if resp.status_code != 200:
            pytest.fail(f"Đăng nhập thất bại ({resp.status_code}): {resp.text}")

        data = resp.json()
        token = data.get("token")
        if not token:
            pytest.fail("Response đăng nhập không trả về JWT token.")
        self.token = token


def find_forbidden_keys(
    data: Any,
    forbidden_keys: set[str],
    current_path: str = "$",
) -> list[str]:
    """Duyệt đệ quy cấu trúc JSON và trả về danh sách đường dẫn chứa trường nhạy cảm."""
    findings: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{current_path}.{key}"
            if key in forbidden_keys:
                findings.append(path)
            findings.extend(find_forbidden_keys(value, forbidden_keys, path))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            findings.extend(find_forbidden_keys(item, forbidden_keys, f"{current_path}[{idx}]"))
    return findings


@pytest.fixture(scope="module")
def auth_client(api_client: Any) -> CrAPIClientAdapter:
    """Khởi tạo client đã xác thực cho tài khoản kiểm thử Lab 03."""
    client = CrAPIClientAdapter(api_client)
    email = os.getenv("CRAPI_TV3_EMAIL", "tv3_data_exposure@example.com")
    password = os.getenv("CRAPI_TV3_PASSWORD", "Password123!")
    name = os.getenv("CRAPI_TV3_NAME", "TV3 Lab03 Tester")
    number = os.getenv("CRAPI_TV3_NUMBER", "9123456780")
    client.authenticate(email=email, password=password, name=name, number=number)
    return client


@pytest.fixture(scope="module")
def sample_post_id(auth_client: CrAPIClientAdapter) -> str:
    """Lấy ID của một bài viết có sẵn hoặc tự tạo bài viết mẫu nếu diễn đàn đang trống."""
    resp = auth_client.get("/community/api/v2/community/posts/recent")
    if resp.status_code == 200:
        body = resp.json()
        posts = body.get("posts", body) if isinstance(body, dict) else body
        if isinstance(posts, list) and len(posts) > 0 and posts[0].get("id"):
            return str(posts[0]["id"])

    create_resp = auth_client.post(
        "/community/api/v2/community/posts",
        json={
            "title": "Lab 03 Seed Post",
            "content": "Seed post for verifying Excessive Data Exposure on community endpoints.",
        },
    )
    if create_resp.status_code not in {200, 201}:
        pytest.fail(f"Không thể tạo bài viết mẫu ({create_resp.status_code}): {create_resp.text}")

    created = create_resp.json()
    post_id = created.get("id")
    if not post_id:
        pytest.fail("Không lấy được post_id sau khi tạo bài viết mẫu.")
    return str(post_id)


@pytest.fixture(scope="module")
def sample_vehicle_id(auth_client: CrAPIClientAdapter) -> str:
    """Lấy vehicle UUID của tài khoản thử nghiệm để kiểm thử endpoint vị trí xe."""
    resp = auth_client.get("/identity/api/v2/vehicle/vehicles")
    if resp.status_code != 200:
        pytest.fail(f"Không thể lấy danh sách xe ({resp.status_code}): {resp.text}")

    vehicles = resp.json()
    if not isinstance(vehicles, list) or len(vehicles) == 0:
        pytest.skip("Tài khoản thử nghiệm chưa được cấp phương tiện (vehicle) trên crAPI.")

    vehicle_id = vehicles[0].get("uuid") or vehicles[0].get("id")
    if not vehicle_id:
        pytest.fail("Không tìm thấy uuid của phương tiện trong response.")
    return str(vehicle_id)


# ---------------------------------------------------------------------------
# 7 Test Cases cho 7 Endpoints thuộc LAB-03: Excessive Data Exposure
# ---------------------------------------------------------------------------

@pytest.mark.security
@pytest.mark.skip(reason="TODO TV3:")
def test_endpoint_1_mechanic_list_does_not_expose_pii(auth_client: CrAPIClientAdapter) -> None:
    """Create a throwaway order, then verify protected fields are server-owned."""
    raise NotImplementedError
