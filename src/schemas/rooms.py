from pydantic import BaseModel, ConfigDict
from src.schemas.facilities import Facilities

class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomsAdd):
    id: int
    model_config = ConfigDict(from_attributes= True)
    

class RoomWithRels(Room):
    facilities: list[Facilities]


class RoomsPatchRequest(BaseModel):
    title: str = None
    description: str | None = None
    price: int = None
    quantity: int = None
    facilities_ids: list[int] = []


class RoomsPatch(BaseModel):
    hotel_id: int
    title: str = None
    description: str | None = None
    price: int = None
    quantity: int = None