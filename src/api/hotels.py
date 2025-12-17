from fastapi import Body, Query, APIRouter 

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPATCH


router = APIRouter(prefix="/hotels", tags= ["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description= "Местоположение отеля"),
    title: str | None = Query(None, description= "Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location= location, 
        title= title, 
        limit= per_page, 
        offset= (pagination.page - 1) * per_page
    )
            
@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int
):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples= {
            "1": {"summary": "Сочи", "value": {
                "title": "Отель Rich 5 звезд у моря",
                "location": "Сочи, ул Моря, 1", 
            }},
            "2": {"summary": "Дубай", "value": {
                "title": "Отель DubaiPlaza у фонтана",
                "location": "Дубай, ул Шейха, 3",
            }}
            })
):
    hotel = await db.hotels.add(hotel_data)

    return {"status": "ok", "data": hotel}
    
@router.delete("/{hotel_id}")
async def del_hotels(
    db: DBDep,
    hotel_id: int
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    
    return {"status": "ok"}

@router.put("/{hotel_id}")
async def edit_hotel(
    db: DBDep,
    hotel_id: int, 
    hotel_data: HotelAdd
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "ok"}

@router.patch("/{id}")

async def change_param(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPATCH
):
    await db.hotels.edit(hotel_data, is_patch= True, id=hotel_id)
    await db.commit()
        
    return {"status": "ok"}

@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int
):
    return await db.hotels.get_one_or_none(id=hotel_id)