from fastapi import APIRouter, Depends, Response

from app.exceptions import (
    CannotAddDataToDatabase,
    UserAlreadyExistsException,
    UserIsNotPresentException,
)
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import SUserAuth, SUserUpdate

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router_users.get("/about_me")
async def get_info_about_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router_users.patch("/edit_user_data")
async def edit_user_data(user: SUserUpdate, current_user: User = Depends(get_current_user)):
    if not current_user:
        raise UserIsNotPresentException    
    values = {k: v for k, v in (user.model_dump()).items() if v is not None}
    password = values.get("password", None)
    email = values.get("email", None)
    if email:
        email_exist = UserDAO.find_one_or_none(email=email)
        if email_exist:
            raise UserAlreadyExistsException       
    if password:
        hashed_password = get_password_hash(user.password)
        del values["password"]
        values["hashed_password"] = hashed_password
    await UserDAO.update(**values, id=current_user["id"])
    return "User data has been updated"


