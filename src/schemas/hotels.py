from pydantic import BaseModel, Field


class Hotel(BaseModel):
    name: str
    title: str
    
class HotelPATCH(BaseModel):
    name: str | None = Field(None)
    title: str | None = Field(None)