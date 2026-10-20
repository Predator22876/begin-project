import pytest

from src.exceptions import LocationNotUniqueException
from src.schemas.hotels import HotelAdd
from src.services.hotels import HotelService


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Hotel 1", location="Сочи")
    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()
    print(f"{new_hotel}")


async def test_add_hotel_with_existing_location_raises_location_not_unique(db):
    hotel_data = HotelAdd(title="Hotel 1", location="Unique test location")
    await HotelService(db).add_hotel(hotel_data)

    with pytest.raises(LocationNotUniqueException):
        await HotelService(db).add_hotel(
            HotelAdd(title="Hotel 2", location="Unique test location")
        )
