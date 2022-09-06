# Python
import os

# FastAPI
from fastapi import status
from fastapi.exceptions import HTTPException

# Utils
import jwt
from passlib.context import CryptContext
from loguru import logger

# Models
from app.core.models.tortoise.user import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config_token = {
    "key": os.getenv("SECRET", ""),
    "algorithm": "HS256"
}


def get_hashed_password(password: str) -> str:
    """ Encrypt password """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password) -> bool:
    """
    An unencrypted password is verified to match an encrypted password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_token(token_data: dict) -> str:
    """
    A json web token is generated
    """
    return jwt.encode(token_data, **config_token)


def decode_jwt(token: str) -> dict:
    """ the payload is decoded from a jason web token """
    return jwt.decode(
        token,
        key=config_token['key'],
        algorithms=config_token['algorithm']
    )


async def verify_token_and_get_user(token: str) -> User:
    """
    Verification of token sent to user's email to confirm account

    @param token: token sent by customer
    """
    try:
        payload = decode_jwt(token=token)
        user = await User.get(id=payload.get("id"))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


async def authenticate_user(username: str, password: str) -> User:
    """
    Is checked to see if the user exists and returned.
    If not found, an error is returned
    """
    user = await User.get(username=username)
    if user and verify_password(password, user.password):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )


async def token_generator(username: str, password: str) -> str:
    """
    A token of the jet type is generated

    @return: User token
    """
    user = await authenticate_user(username, password)
    token_data = {
        "id": user.id,
        "username": user.username,
    }
    return get_token(token_data)
