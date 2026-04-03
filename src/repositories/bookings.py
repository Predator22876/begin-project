from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
