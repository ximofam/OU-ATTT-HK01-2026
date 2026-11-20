
"""LAB-02: BFLA — regular users must not invoke admin video deletion."""

import os

import pytest


@pytest.mark.security
def test_regular_user_cannot_invoke_admin_video_delete(api_client):
    """A ROLE_USER token must be rejected by the admin-only delete endpoint.

    Uses a non-existent video ID to ensure no lab data is deleted.
    """
    user_email = os.environ.get(
        "CRAPI_BFLA_USER_EMAIL", "tester.lab@example.com"
    )
    user_password = os.environ.get("CRAPI_BFLA_USER_PASSWORD")

    assert user_password, (
        "Set CRAPI_BFLA_USER_PASSWORD in your local .env file"
    )

    # 1. Đăng nhập bằng tài khoản thường
    login = api_client.post(
        "/identity/api/auth/login",
        json={"email": user_email, "password": user_password},
    )
    assert login.status_code == 200, (
        f"Regular user login failed: HTTP {login.status_code}"
    )

    token = login.json()["token"]

    # 2. Gọi chức năng xóa video dành riêng cho Admin.
    # ID 999999 là ID giả, không dùng video thật.
    response = api_client.delete(
        "/identity/api/v2/admin/videos/999999",
        headers={"Authorization": f"Bearer {token}"},
    )

    # 3. ROLE_USER phải bị từ chối bởi lớp phân quyền.
    assert response.status_code == 403, (
        "BFLA protection failed: expected HTTP 403 for ROLE_USER, "
        f"got HTTP {response.status_code}: {response.text}"
    )
