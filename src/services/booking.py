from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.services.base import BaseService


class BookingService(BaseService):
    async def create_booking(
        self, user_id: int, data: BookingAddRequest
    ):
        try:
            room = await self.db.rooms.get_one(id=data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id, price=room_price, **data.model_dump()
        )
        await self.db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
        await self.db.commit()

    async def get_booking(self):
        return await self.db.bookings.get_all()
    
    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)