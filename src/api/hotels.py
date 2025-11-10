from fastapi import Body, Query, APIRouter 

from sqlalchemy import insert, select, func

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
        query = select(HotelsOrm)

        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.strip().lower()}%"))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.strip().lower()}%"))
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        print(query.compile(compile_kwargs = {"literal_binds": True}))
        result = await session.execute(query)
        
        hotels = result.scalars().all()
        # print(type(hotels), hotels)
        return hotels
    
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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})) #дебаг строчка - возвращает sql запрос
        await session.execute(add_hotel_stmt)
        await session.commit()
      
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
