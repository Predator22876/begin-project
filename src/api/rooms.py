from fastapi import APIRouter, Body, HTTPException, Query
from datetime import date

from src.exceptions import (
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    RoomNotFoundHTTPException,
    check_date_to_after_date_from,
)
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, RoomsPatch
from src.schemas.facilities import RoomsFacilitiesAdd
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
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    if room_data.facilities_ids:
        rooms_facilities_data = [
            RoomsFacilitiesAdd(room_id=room.id, facilities_id=f_id)
            for f_id in room_data.facilities_ids
        ]

    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "ok", "data": room}


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
):
    check_date_to_after_date_from(date_from, date_to)
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.detail)


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep, hotel_id: int, room_id: int, room_new_data: RoomsAddRequest
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_new_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.set_room_facilities(
        room_id, facilities_ids=room_new_data.facilities_ids
    )

    await db.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room_params(
    db: DBDep, hotel_id: int, room_id: int, room_new_data: RoomsPatchRequest
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    _room_data_dict = room_new_data.model_dump(exclude_unset=True)
    _room_data = RoomsPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, is_patch=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )

    await db.commit()

    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_rooms(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}
