# FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.params import Depends

# Models
from app.core.models.tortoise.user import User

# Utils
from app.utils.api.authentication import verify_token_and_get_user

oath2_schema = OAuth2PasswordBearer(tokenUrl="user/token")


async def get_current_user(token: str = Depends(oath2_schema)) -> User:
    user = await verify_token_and_get_user(token=token)
    return user
