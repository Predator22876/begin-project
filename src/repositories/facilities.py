from sqlalchemy import select, delete, insert

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facilities
from src.repositories.mappers.mappers import FacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = Facilities
    
    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        get_cur_facilities_ids_query = (
            select(self.model.facilities_id)
            .filter_by(room_id = room_id)
        )
        res = await self.session.execute(get_cur_facilities_ids_query)
        cur_facilities_ids = res.scalars().all()
        
        ids_to_delete = list(set(cur_facilities_ids) - set(facilities_ids))
        ids_to_insert = list(set(facilities_ids) - set(cur_facilities_ids))
        
        if ids_to_delete:
            delete_m2m_facilities_stmt = (
               delete(self.model)
               .filter(
                   self.model.room_id == room_id,
                   self.model.facilities_id.in_(ids_to_delete)
                )
            )
            
            await self.session.execute(delete_m2m_facilities_stmt)
        
        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values(
                    [{"room_id": room_id, "facilities_id": f_id} for f_id in ids_to_insert]
                )
            )
            
            await self.session.execute(insert_m2m_facilities_stmt)
            