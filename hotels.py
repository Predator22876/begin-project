from fastapi import Body, Query, APIRouter 

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags= ["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description= "Айди"),
    title: str | None = Query(None, description= "Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]
    return hotels_

@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples= {
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya", 
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "name": "dubai_fountain",
    }}
    })
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "ok"}
    
@router.delete("/{hotel_id}")
def del_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "ok"}

@router.put("/{hotel_id}")
def change_hotel(
    hotel_id: int, 
    hotel_data: Hotel
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["name"] = hotel_data.name
            hotel["title"] = hotel_data.title
            return hotel
    return {"status": "object is not finded"}

@router.patch("/{id}")
def change_param(
    id: int,
    hotel_data: HotelPATCH
):
    for hotel in hotels:
        if hotel["id"] == id:
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if not (hotel_data.name or hotel_data.title):
                return {"status": "object parameters have not modified"}
            return hotel
    return {"status": "object is not finded"}
