from fastapi import APIRouter, Body

from src.repositories.rooms import RoomsRepository

from src.database import async_session_maker
from src.schemas.rooms import RoomsAdd, RoomsAddRequest

router = APIRouter(prefix= "/hotels", tags= ["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()

@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    room_data: RoomsAddRequest = Body(openapi_examples={
        "1": {"summary": "Люкс", "value": {
            "title": "Лучший номер ever",
            "price": 50000,
            "description": "Номер крутой",
            "quantity": 3
        }}
    })
):
    _room_data = RoomsAdd(hotel_id= hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "ok", "data": room}    
    