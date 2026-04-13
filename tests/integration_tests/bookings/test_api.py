import pytest

@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-04-12", "2026-04-13", 200),
    (1, "2026-04-12", "2026-04-13", 200),
    (1, "2026-04-12", "2026-04-13", 200),
    (1, "2026-04-12", "2026-04-13", 200),
    (1, "2026-04-12", "2026-04-13", 200),
    (1, "2026-04-12", "2026-04-13", 500),
])
async def test_add_booking(room_id, date_from, date_to, status_code, db, authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json = {
            "room_id": room_id,
            "date_from": date_from,
            "date_to" : date_to
        }
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res