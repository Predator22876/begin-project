from fastapi import APIRouter, Body, Query
from datetime import date

from src.services.rooms import RoomServise
from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.rooms import RoomsAddRequest, RoomsPatchRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomsAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Люкс",
                "value": {
                    "title": "Лучший номер ever",
                    "price": 50000,
                    "description": "Номер крутой",
                    "quantity": 3,
                    "facilities_ids": [],
                },
            }
        }
    ),
):
    try:
        room = await RoomServise(db).add_room(hotel_id=hotel_id, data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok", "data": room}


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
):
    return await RoomServise(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        RoomServise(db).get_rooms(hotel_id=hotel_id, id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep, hotel_id: int, room_id: int, room_new_data: RoomsAddRequest
):
    await RoomServise(db).edit_room(
        hotel_id=hotel_id,
        id = room_id,
        new_data=room_new_data,
    )
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room_params(
    db: DBDep, hotel_id: int, room_id: int, room_new_data: RoomsPatchRequest
):
    await RoomServise(db).edit_room_params(
        hotel_id=hotel_id,
        id = room_id,
        new_data=room_new_data,
    )

    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_rooms(db: DBDep, hotel_id: int, room_id: int):
    await RoomServise(db).delete_rooms(hotel_id=hotel_id, id=room_id)
    return {"status": "ok"}
