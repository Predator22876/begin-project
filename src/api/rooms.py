from fastapi import APIRouter, Body

from src.repositories.rooms import RoomsRepository

from src.database import async_session_maker
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPATCH

router = APIRouter(prefix= "/hotels", tags= ["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id= room_id, hotel_id= hotel_id)

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

@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_rooms(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "ok"}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_new_data: RoomsAddRequest
):
    _room_data = RoomsAdd(hotel_id= hotel_id, **room_new_data.model_dump())
    async with async_session_maker() as session:
        new_room = await RoomsRepository(session).edit(_room_data, id= room_id)
        await session.commit()
    
    return {"status": "ok"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room_params(
    hotel_id: int,
    room_id: int,
    room_new_data: RoomsPATCH
):
    _room_data = RoomsAdd(hotel_id= hotel_id, **room_new_data.model_dump())
    async with async_session_maker() as session:
        new_room = await RoomsRepository(session).edit(_room_data, is_patch=True, id= room_id)
        await session.commit()
    
    return {"status": "ok"}

