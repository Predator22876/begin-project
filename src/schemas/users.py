from pydantic import BaseModel, EmailStr, ConfigDict

    
class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserRequestAddWithName(UserRequestAdd):
    first_name: str
    last_name: str


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserWithHashedPassword(User):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)