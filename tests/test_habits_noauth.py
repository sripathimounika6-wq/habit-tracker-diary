import json

from app.main import create_app


def test_habit_diary_flow():
    app = create_app()
    client = app.test_client()

    headers = {
      "X-User-Id": "test_user",
      "Content-Type": "application/json",
    }

    payload = {
        "title": "Test Entry",
        "frequency": "one-off",
        "notes": "note1",
        "date": "2025-12-05",
    }

    # create entry
    resp = client.post(
        "/api/habits",
        headers=headers,
        data=json.dumps(payload),
    )
    assert resp.status_code == 201
    habit = resp.get_json()
    assert habit["title"] == "Test Entry"
    hid = habit["id"]

    # toggle done
    resp = client.put(
        f"/api/habits/{hid}",
        headers=headers,
        data=json.dumps({"done": True}),
    )
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated.get("done") is True

    # list
    resp = client.get("/api/habits", headers={"X-User-Id": "test_user"})
    assert resp.status_code == 200
    items = resp.get_json()
    assert any(item["id"] == hid for item in items)
