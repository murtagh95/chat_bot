""" User router """
# Python
import secrets

# FastAPI
from fastapi import File, UploadFile
# from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

# Config
from app.config.oath import get_current_user
from app.config.template import templates

# Models
from app.core.models.tortoise.user import User, user_pydantic_in, user_pydantic
from app.core.models.tortoise.business import Business, business_pydantic

# Utils
from PIL import Image
from app.utils.api.authentication import (
    get_hashed_password,
    verify_token_and_get_user,
    token_generator
)
from app.utils.email import send_email
from typing import List, Optional, Type

# Tortoise
from tortoise.signals import post_save
from tortoise.backends.base.client import BaseDBAsyncClient


router = APIRouter()


# Signals
@post_save(User)
async def create_business(
        sender: "Type[User]",
        instance: User,
        created: bool,
        using_db: "Optional[BaseDBAsyncClient]",
        update_fields: List[str]
) -> None:
    if created:
        business_obj = await Business.create(
            name=instance.username,
            owner=instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)
        await send_email(email=[instance.email], instance=instance)


@router.post("/registration",
             description="User registration",
             response_description="User")
async def user_registration(user: user_pydantic_in):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = get_hashed_password(user_info['password'])
    user_obj = await User.create(**user_info)
    await user_pydantic.from_tortoise_orm(user_obj)
    return {
        "message": "User create"
    }


@router.get("/verification",
            response_class=HTMLResponse,
            description="User verification")
async def email_verification(request: Request, token: str):
    user = await verify_token_and_get_user(token=token)
    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse(
            "verification.html", {"request": request, "user": user})

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )


@router.post('/token')
async def generate_token(
        request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "bearer"}


@router.get('/me')
async def user_login(
        user: user_pydantic_in = Depends(get_current_user)):
    business = await Business.get(owner=user)
    return {
        "status": "ok",
        "data": {
            "username": user.username,
            "email": user.email,
            "verified": user.is_verified,
            "join_date": user.join_date.strftime("%b %d %Y"),
            "business": await business_pydantic.from_tortoise_orm(business)
        }
    }


@router.post("uploadfile")
async def create_upload_file(
        file: UploadFile = File(...),
        user: user_pydantic_in = Depends(get_current_user)
):
    extension = file.filename.split(".")[1]
    if extension not in ["png", "jpg"]:
        return {
            "status": "error",
            "detail": "File extension not allowed"
        }
    token_name = f"{secrets.token_hex(10)}.{extension}"
    generated_name = f"./public/images/{token_name}"
    file_content = await file.read()

    with open(generated_name, "wb") as file_generated:
        file_generated.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save()

    file_generated.close()
    business = await Business.get(owner=user)
    owner = business.owner

    if owner == user:
        business.logo = token_name
        await business.save()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated to perform this action",
            headers={"WWW-Authenticate": "Bearer"}
        )
