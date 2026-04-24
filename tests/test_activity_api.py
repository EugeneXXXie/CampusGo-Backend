def test_create_and_list_activity(client) -> None:
    login = client.post("/api/auth/login", json={"phone": "18800001111", "password": "123456"})
    token = login.json()["data"]["access_token"]

    create_response = client.post(
        "/api/activities",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "category_id": 1,
            "title": "周末自习局",
            "cover": "",
            "description": "图书馆一起复习",
            "activity_time": "2026-05-01T14:00:00",
            "location": "图书馆四楼",
            "max_participants": 6,
            "audit_required": False,
            "contact_info": "微信 test",
        },
    )
    assert create_response.status_code == 200

    list_response = client.get("/api/activities")
    assert list_response.status_code == 200
    assert list_response.json()["data"]["total"] >= 1
