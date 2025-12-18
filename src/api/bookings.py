from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep
from src.models.bookings import BookingsOrm


router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.post("/{room_id}")
async def create_booking(
    db: DBDep,
    room_id: int,
    user_id: UserIdDep,
    price: int,
    booking_data: BookingAddRequest
):
    #ну ваще хз че в price писать
    _booking_data = BookingAdd(user_id=user_id, room_id=room_id, price=5000, **booking_data.model_dump)
    await db.bookings.add(_booking_data)
    await db.commit()