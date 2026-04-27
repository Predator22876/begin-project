from datetime import date

from fastapi import HTTPException


class MyAppException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyAppException):
    detail = "Объект не найлен"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найлен"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найлен"

class AllRoomsAreBookedException(ObjectNotFoundException):
    detail = "Не осталось свободных номеров"

class UserAlreadyExists(ObjectNotFoundException):
    detail = "Пользователь уже зарегистрирован"

class CheckInDateLaterThanCheckOutDate(ObjectNotFoundException):
    detail = "Дата заезда позже даты выезда"


class CheckInDateEqualCheckOutDate(ObjectNotFoundException):
    detail = "Дата заезда равна дате выезда"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422,
            detail="Дата заезда не может быть позже даты выезда или равна ей",
        )


class MyAppHTTPException(HTTPException):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "Номер не найден"
