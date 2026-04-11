from src.database import async_session_maker
from src.schemas.hotels import HotelAdd
from utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 1", location="Сочи")
    async with DBManager(session_factory= async_session_maker) as db:
        new_hotel = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel}")