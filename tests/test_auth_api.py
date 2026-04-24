def test_register_login_and_me(client) -> None:
    register_response = client.post(
        "/api/auth/register",
        json={
            "phone": "18800002222",
            "password": "123456",
            "nickname": "测试同学",
        },
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/api/auth/login",
        json={"phone": "18800002222", "password": "123456"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]

    me_response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["data"]["phone"] == "18800002222"
