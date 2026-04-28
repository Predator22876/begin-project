from fastapi import APIRouter, Response

from src.exceptions import EmailNotRegisteredException, EmailNotRegisteredHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException, UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException
from src.schemas.users import UserRequestAdd, UserRequestAddWithName
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(user_data: UserRequestAddWithName, db: DBDep):
    try:
        await AuthService(db).register_user(data=user_data)
    except UserAlreadyExistsException as ex:  
        raise UserEmailAlreadyExistsHTTPException from ex
        
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    user_data: UserRequestAdd,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data=user_data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    return await AuthService(db).get_me(id=user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
