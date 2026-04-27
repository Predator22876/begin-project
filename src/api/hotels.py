from fastapi import Body, Query, APIRouter
from datetime import date

from src.services.hotels import HotelService
from src.exceptions import (
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
)
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPatch


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Rich 5 звезд у моря",
                    "location": "Сочи, ул Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель DubaiPlaza у фонтана",
                    "location": "Дубай, ул Шейха, 3",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "ok", "data": hotel}


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
    location: str | None = Query(None, description="Местоположение отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        date_from,
        date_to,
        location,
        title,
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    HotelService(db).edit_hotel(id=hotel_id, data=hotel_data)
    return {"status": "ok"}


@router.patch("/{hotel_id}")
async def change_param(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    HotelService(db).change_params(id=hotel_id, data=hotel_data)
    return {"status": "ok"}


@router.delete("/{hotel_id}")
async def del_hotels(db: DBDep, hotel_id: int):
    HotelService(db).delete_hotels(id=hotel_id)
    return {"status": "ok"}
