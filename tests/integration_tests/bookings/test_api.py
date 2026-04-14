import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-04-12", "2026-04-13", 200),
        (1, "2026-04-12", "2026-04-13", 200),
        (1, "2026-04-12", "2026-04-13", 200),
        (1, "2026-04-12", "2026-04-13", 200),
        (1, "2026-04-12", "2026-04-13", 200),
        (1, "2026-04-12", "2026-04-13", 409),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2026-04-12", "2026-04-13", 1),
        (1, "2026-04-12", "2026-04-13", 2),
        (1, "2026-04-12", "2026-04-13", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, booked_rooms, delete_all_bookings, authenticated_ac
):
    add_response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert add_response.status_code == 200

    get_response = await authenticated_ac.get(
        "/bookings/me",
    )
    assert get_response.status_code == 200
    assert len(get_response.json()) == booked_rooms
