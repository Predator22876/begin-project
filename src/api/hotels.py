from fastapi import Body, Query, APIRouter 

from sqlalchemy import insert, select, func

from repositories.hotels import HotelsRepository
from src.models.hotels import HotelsOrm
from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags= ["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description= "Местоположение отеля"),
    title: str | None = Query(None, description= "Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location= location, 
            title= title, 
            limit= per_page, 
            offset= (pagination.page - 1) * per_page
        )
            
@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples= {
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "ул Моря, 1", 
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "location": "ул Моря, 3",
    }}
    })
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "ok", "data": hotel}
    
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
