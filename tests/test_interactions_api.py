def test_comment_reply_favorite_and_read_message(client) -> None:
    owner_login = client.post("/api/auth/login", json={"phone": "18800001111", "password": "123456"})
    owner_token = owner_login.json()["data"]["access_token"]

    client.post(
        "/api/auth/register",
        json={"phone": "18800004444", "password": "123456", "nickname": "互动同学"},
    )
    user_login = client.post("/api/auth/login", json={"phone": "18800004444", "password": "123456"})
    user_token = user_login.json()["data"]["access_token"]

    activity = client.post(
        "/api/activities",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "category_id": 1,
            "title": "互动活动",
            "cover": "",
            "description": "评论收藏联动测试",
            "activity_time": "2026-05-03T10:00:00",
            "location": "教学楼",
            "max_participants": 5,
            "audit_required": False,
            "contact_info": "微信 owner",
        },
    ).json()["data"]

    favorite = client.post(
        f"/api/activities/{activity['id']}/favorite",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert favorite.status_code == 200
    assert favorite.json()["data"]["is_favorite"] is True

    root_comment = client.post(
        f"/api/activities/{activity['id']}/comments",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"content": "欢迎来玩"},
    ).json()["data"]

    reply = client.post(
        f"/api/activities/{activity['id']}/comments",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"content": "我来啦", "parent_id": root_comment["id"]},
    )
    assert reply.status_code == 200

    owner_messages = client.get("/api/messages", headers={"Authorization": f"Bearer {owner_token}"})
    assert owner_messages.status_code == 200
    first_message_id = owner_messages.json()["data"][0]["id"]

    read_response = client.post(
        f"/api/messages/read/{first_message_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert read_response.status_code == 200
    assert read_response.json()["data"]["is_read"] is True
