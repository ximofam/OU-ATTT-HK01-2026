"""LAB-01: BOLA — access to another user's vehicle resource."""

import os

import pytest


@pytest.mark.security
def test_user_cannot_read_another_users_vehicle(api_client):
    """Set up A/B accounts; send user A's token for a vehicle belonging to B.

    Assert the expected authorization policy and document actual behavior.
    """
    user_a_email = os.environ.get("CRAPI_USER_A_EMAIL", "usera@example.com")
    user_a_password = os.environ.get("CRAPI_USER_A_PASSWORD", "Usera@123")
    user_b_email = os.environ.get("CRAPI_USER_B_EMAIL", "userb@example.com")
    user_b_password = os.environ.get("CRAPI_USER_B_PASSWORD", "Userb@123")

    # 1. Đăng nhập User A và lấy access token
    login_a = api_client.post(
        "/identity/api/auth/login",
        json={"email": user_a_email, "password": user_a_password},
    )
    assert login_a.status_code == 200, f"User A login failed: {login_a.text}"
    token_a = login_a.json()["token"]

    # 2. Đăng nhập User B và lấy danh sách phương tiện thuộc về User B
    login_b = api_client.post(
        "/identity/api/auth/login",
        json={"email": user_b_email, "password": user_b_password},
    )
    assert login_b.status_code == 200, f"User B login failed: {login_b.text}"
    token_b = login_b.json()["token"]

    vehicles_b_resp = api_client.get(
        "/identity/api/v2/vehicle/vehicles",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert vehicles_b_resp.status_code == 200, "Failed to fetch User B vehicles"
    vehicles_b = vehicles_b_resp.json()
    assert len(vehicles_b) > 0, "User B must have at least one activated vehicle"
    target_vehicle_id = vehicles_b[0]["uuid"]

    # 3. Kiểm chứng phân quyền: dùng token của User A truy vấn tọa độ xe của User B
    unauthorized_resp = api_client.get(
        f"/identity/api/v2/vehicle/{target_vehicle_id}/location",
        headers={"Authorization": f"Bearer {token_a}"},
    )

    # Chính sách bảo mật chuẩn: server phải từ chối truy cập chéo đối tượng
    assert unauthorized_resp.status_code in {401, 403, 404}, (
        f"BOLA detected: expected 401/403/404 when User A reads User B's vehicle "
        f"({target_vehicle_id}), but got {unauthorized_resp.status_code}: "
        f"{unauthorized_resp.text}"
    )