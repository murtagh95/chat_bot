# Utils
from pydantic import BaseModel, Field

# Models
from app.core.models.pydantic.button_pydantic import (
    ButtonPydantic,
    ButtonPydanticWithId
)


class CardPydantic(BaseModel):
    """ Card pydantic """
    text: str = Field(title="Text to go on the button", max_length=500)
    url_image: str = Field(
        title="value received when selecting the button", max_length=200)
    button_list_card: list[ButtonPydantic]


class CardPydanticWithId(BaseModel):
    """ Card pydantic """
    id: int
    text: str = Field(title="Text to go on the button", max_length=500)
    url_image: str = Field(
        title="value received when selecting the button", max_length=200)
    button_list_card: list[ButtonPydanticWithId]
