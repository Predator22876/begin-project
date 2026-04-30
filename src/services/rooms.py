from datetime import date
from src.schemas.facilities import RoomsFacilitiesAdd
from src.services.hotels import HotelService
from src.schemas.rooms import Room, RoomsAdd, RoomsAddRequest, RoomsPatch, RoomsPatchRequest
from src.exceptions import ObjectNotFoundException, RoomNotFoundException, check_date_to_after_date_from
from src.services.base import BaseService


class RoomServise(BaseService):
    async def get_filtered_by_time(
        self, 
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    
    async def get_room(self, hotel_id: int, id: int):
        return await self.db.rooms.get_one_or_none(id=id, hotel_id=hotel_id)
    
    async def add_room(
        self,
        hotel_id: int,
        data: RoomsAddRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        _room_data = RoomsAdd(hotel_id=hotel_id, **data.model_dump())
        room = await self.db.rooms.add(_room_data)

        if data.facilities_ids:
            rooms_facilities_data = [
                RoomsFacilitiesAdd(room_id=room.id, facilities_id=f_id)
                for f_id in data.facilities_ids
            ]

        if rooms_facilities_data:
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
    
    async def edit_room(
        self,
        hotel_id: int, 
        id: int, 
        new_data: RoomsAddRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        
        await self.get_room_with_check(id=id)
        _room_data = RoomsAdd(hotel_id=hotel_id, **new_data.model_dump())
        await self.db.rooms.edit(_room_data, id=id, hotel_id=hotel_id)
        await self.db.rooms_facilities.set_room_facilities(
            id, facilities_ids=new_data.facilities_ids
        )

        await self.db.commit()

    async def edit_room_params(
        self,
        hotel_id: int, 
        id: int, 
        new_data: RoomsPatchRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(id=id)
        _room_data_dict = new_data.model_dump(exclude_unset=True)
        _room_data = RoomsPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(_room_data, is_patch=True, id=id, hotel_id=hotel_id)
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                id, facilities_ids=_room_data_dict["facilities_ids"]
            )

        await self.db.commit()

    async def delete_rooms(self, hotel_id: int, id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(id=id)
        await self.db.rooms.delete(id=id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            await self.db.rooms.get_one(id=id)
        except ObjectNotFoundException:
            raise RoomNotFoundException