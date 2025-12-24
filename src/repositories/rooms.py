from datetime import date

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from src.repositories.utils import rooms_ids_for_booking

'''
with rooms_count as (
    select room_id, count(*) as rooms_booked from bookings
    where date_from <= '2024-11-07' and date_to >= '2024-07-01'
    group by room_id
),
rooms_left_table as (
    select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
    from rooms
    left join rooms_count on rooms.id = rooms_count.room_id
)
select * from rooms_left_table
where rooms_left > 0
;
'''

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room
    
    async def get_filterd_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, 
            date_to=date_to, 
            hotel_id=hotel_id,
        )

        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))