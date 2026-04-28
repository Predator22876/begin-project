from fastapi import APIRouter

from src.services.booking import BookingService
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest
from src.api.dependencies import DBDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest
):
    try:
        booking = await BookingService(db).create_booking(user_id=user_id, data=booking_data)
    except AllRoomsAreBookedException as ex:
        raise AllRoomsAreBookedHTTPException from ex

    return {"status": "OK", "data": booking}


@router.get("")
async def get_booking(
    db: DBDep,
):
    return await BookingService(db).get_booking()


@router.get("/me")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id=user_id)
