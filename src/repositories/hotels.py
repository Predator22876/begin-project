from sqlalchemy import select, func

from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm

from src.repositories.utils import rooms_ids_for_booking

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel
        
    async def get_filtered_by_time(
            self,
            location,
            title,
            limit,
            offset,    
            date_from: int,
            date_to: int,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotel_ids_to_booking = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotel_ids_to_booking))

        if location:
            query = query.filter(func.lower(HotelsOrm.location)
                                 .contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title)
                                 .contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
        