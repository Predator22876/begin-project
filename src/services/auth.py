from datetime import datetime, timezone, timedelta
from src.exceptions import EmailNotRegisteredException, IncorrectPasswordException, ObjectAlreadyExistsException, UserAlreadyExistsException
from src.schemas.users import UserAdd, UserRequestAdd, UserRequestAddWithName
from src.services.base import BaseService
from src.config import settings

from passlib.context import CryptContext
import jwt


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, token: str) -> dict:
        return jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

    async def register_user(self, data: UserRequestAddWithName):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(
            email=data.email,
            hashed_password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException

    async def login_user(
        self,
        data: UserRequestAdd,
    ):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        
        access_token = self.create_access_token({"user_id": user.id})
        return access_token
    
    async def get_me(
        self,
        id: int,
    ):
        return await self.db.users.get_one_or_none(id=id)