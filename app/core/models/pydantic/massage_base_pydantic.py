# Python
from pydantic import BaseModel, HttpUrl, Field

# Models
from app.core.models.tortoise.message import MessageEnum


class MessageBase(BaseModel):
    """ Message base BaseModel """
    type: MessageEnum
    text: str
    url: HttpUrl | None = Field(default=None, title="Url of an image")


class MessageBaseWithID(MessageBase):
    """ Message base BaseModel """
    id: int
