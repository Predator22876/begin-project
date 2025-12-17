from fastapi import APIRouter, HTTPException, Response, Request

from src.schemas.users import UserAdd, UserRequestAdd, UserRequestAddWithName
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(
        data: UserRequestAddWithName,
        db: DBDep
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        email= data.email, 
        hashed_password= hashed_password,
        first_name=data.first_name,
        last_name=data.last_name
    )
    db.users.add(new_user_data)
    await db.commit()
        
    return {"status": "OK"}

@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}
    

@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
        user = await db.users.get_one_or_none(id=user_id)
        return user

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}