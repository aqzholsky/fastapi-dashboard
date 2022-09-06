from datetime import timedelta

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.server.models import (ErrorResponseModel, Token, UserLogin,
                               UserRegistration)
from app.server.repository import (ACCESS_TOKEN_EXPIRE_MINUTES,
                                   authenticate_user, create_access_token,
                                   create_user, get_user,
                                   retrieve_random_company)

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(request: UserLogin = Body(...)):
    login_data = jsonable_encoder(request)

    user = await authenticate_user(login_data["username"], login_data["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_user(request: UserRegistration = Body(...)):
    user_data = jsonable_encoder(request)

    old_user = await get_user(user_data["username"])
    if old_user:
        return ErrorResponseModel("An error occurred.", 401, "User already exists!")

    if user_data["password1"] != user_data["password2"]:
        return ErrorResponseModel("An error occurred.", 401, "Invalid password!")
    del user_data["password2"]

    if not user_data.get("company_id"):
        company = await retrieve_random_company()
        user_data["company_id"] = company["id"]
    else:
        user_data["company_id"] = user_data["company_id"]

    new_user = await create_user(user_data)
    del new_user["hashed_password"]
    return new_user
