from pydantic import BaseModel, ConfigDict


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomsAdd):
    id: int
    
    model_config = ConfigDict(from_attributes= True)


class RoomsPATCH(BaseModel):
    title: str = None
    description: str | None = None
    price: int = None
    quantity: int = None