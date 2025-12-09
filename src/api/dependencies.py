from typing import Annotated

<<<<<<< HEAD
from fastapi import Depends, Query, HTTPException
from starlette.requests import Request
=======
from fastapi import Depends, Query, HTTPException, Request
>>>>>>> 4f82cfedc3ca5d57e8bedba9ab72f4e63c02f5fb
from pydantic import BaseModel

from src.services.auth import AuthService

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description= "Номер страницы", ge= 1)]
    per_page: Annotated[int | None, Query(None, description= "Количетство отелей на странице", ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]