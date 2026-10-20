from datetime import date

from sqlalchemy import Boolean
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
from src.exceptions import (
    HotelNotFoundException, 
    ObjectNotFoundException, 
    check_date_to_after_date_from, 
    EmptySlotsException,
    LocationNotUniqueException
)
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination,
            date_from: date,
            date_to: date,
            location: str | None,
            title: str | None,
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            location=location,
            title=title,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
            date_from=date_from,
            date_to=date_to,
        )
    
    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)
    
    async def add_hotel(self, data: HotelAdd):
        if self.check_unique_location(data.location):
            hotel = await self.db.hotels.add(data)
            await self.db.commit()
            return hotel
        else:
            raise LocationNotUniqueException
        
    async def edit_hotel(self, data: HotelAdd, id: int):
        await self.get_hotel_with_check(id=id)
        await self.db.hotels.edit(data, id=id)
        await self.db.commit()
    
    async def change_params(self, data: HotelPatch, id: int):
        await self.get_hotel_with_check(id=id)
        _hotel_data_dict = data.model_dump(exclude_unset=True)
        if not _hotel_data_dict:
            raise EmptySlotsException
        _hotel_data = HotelPatch(**_hotel_data_dict)
        await self.db.hotels.edit(_hotel_data, is_patch=True, id=id)
        await self.db.commit()
    
    async def delete_hotels(self, id: int):
        await self.get_hotel_with_check(id=id)
        await self.db.hotels.delete(id=id)
        await self.db.commit()
    
    async def get_hotel_with_check(self, id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
    
    async def check_unique_location(self, location: str) -> bool:
        try:
            await self.db.hotels.get_one(location)
            return False
        except ObjectNotFoundException:
            return True

    
