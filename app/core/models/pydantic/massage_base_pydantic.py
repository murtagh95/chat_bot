# Python
from pydantic import BaseModel, HttpUrl, Field, root_validator

# Models
from app.core.models.tortoise.message import MessageEnum

# Utils
from app.utils.api.constants import (
    ERROR_FIELD_NOT_REQUIRED,
    ERROR_REQUIRED_FIELD)


def validate_url_according_type(values: dict):
    """
    It is validated that the url is not sent for certain types of messages.
    """
    type_message: MessageEnum = values['type']
    if type_message in [MessageEnum.LIST_OF_BUTTONS,
                        MessageEnum.LIST_OF_CARDS, MessageEnum.TEXT_ONLY]:
        if "url" in values and values["url"] is not None:
            raise ValueError(ERROR_FIELD_NOT_REQUIRED.format(
                field="url", type=type_message.value))

    if type_message in [MessageEnum.TEXT_AND_IMAGE,
                        MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
        if "url" not in values or values["url"] is None:
            raise ValueError(ERROR_REQUIRED_FIELD.format(
                field="url", type=type_message.value))


class MessageBase(BaseModel):
    """ Message base BaseModel """
    type: MessageEnum
    text: str
    url: HttpUrl | None = Field(default=None, title="Url of an image")

    @root_validator(pre=False)
    def check_url(cls, values: dict):
        """ The url is verified. """
        if "type" not in values:
            # If the guy doesn't come I let pydantic return an error.
            return values
        validate_url_according_type(values=values)

        return values


class MessageBaseWithID(MessageBase):
    """ Message base BaseModel """
    id: int
