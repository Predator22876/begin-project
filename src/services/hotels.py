from datetime import date
from src.schemas.hotels import HotelAdd, HotelPatch
from src.exceptions import check_date_to_after_date_from
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
        await self.db.hotels.add(data)
        await self.db.commit()
    
    async def edit_hotel(self, data: HotelAdd, id: int):
        await self.db.hotels.edit(data, id=id)
        await self.db.commit()
    
    async def change_params(self, data: HotelPatch, id: int):
        await self.db.hotels.edit(data, is_patch=True, id=id)
        await self.db.commit()
    
    async def delete_hotels(self, id: int):
        await self.db.hotels.delete(id=id)
        await self.db.commit()