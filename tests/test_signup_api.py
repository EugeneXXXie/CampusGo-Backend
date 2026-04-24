def test_signup_pending_and_message_created(client) -> None:
    owner_login = client.post("/api/auth/login", json={"phone": "18800001111", "password": "123456"})
    owner_token = owner_login.json()["data"]["access_token"]

    client.post(
        "/api/auth/register",
        json={"phone": "18800003333", "password": "123456", "nickname": "报名同学"},
    )
    user_login = client.post("/api/auth/login", json={"phone": "18800003333", "password": "123456"})
    user_token = user_login.json()["data"]["access_token"]

    activity = client.post(
        "/api/activities",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "category_id": 1,
            "title": "需审核活动",
            "cover": "",
            "description": "需要审核的报名活动",
            "activity_time": "2026-05-02T10:00:00",
            "location": "操场",
            "max_participants": 5,
            "audit_required": True,
            "contact_info": "微信 owner",
        },
    ).json()["data"]

    signup = client.post(
        f"/api/activities/{activity['id']}/signup",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert signup.status_code == 200
    assert signup.json()["data"]["status"] == "pending"

    messages = client.get("/api/messages", headers={"Authorization": f"Bearer {owner_token}"})
    assert messages.status_code == 200
    assert len(messages.json()["data"]) == 1
