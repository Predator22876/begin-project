from fastapi import APIRouter, Body, Query
from datetime import date

from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, RoomsPatch
from src.api.dependencies import DBDep

router = APIRouter(prefix= "/hotels", tags= ["Номера"])

@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
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
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "ok", "data": room}

  
@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)



@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_new_data: RoomsAddRequest
):
    _room_data = RoomsAdd(hotel_id= hotel_id, **room_new_data.model_dump())
    await db.rooms.edit(_room_data, id= room_id, hotel_id=hotel_id)
    await db.commit()
    
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room_params(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_new_data: RoomsPatchRequest
):
    _room_data = RoomsPatch(hotel_id= hotel_id, **room_new_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, is_patch=True, id= room_id, hotel_id=hotel_id)
    await db.commit()
    
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_rooms(
    db: DBDep,
    hotel_id: int,
    room_id: int
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}