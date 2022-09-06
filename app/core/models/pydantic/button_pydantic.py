# Utils
from pydantic import BaseModel, Field


class ButtonPydantic(BaseModel):
    text: str = Field(
        title="Text to go on the button", max_length=500)
    value: str = Field(
        title="value received when selecting the button", max_length=200)
