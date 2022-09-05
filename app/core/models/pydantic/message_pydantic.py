""" New message base model """
# Utils
from pydantic import BaseModel, Field, HttpUrl, root_validator

# Models
from app.core.models.tortoise.message import MessageEnum


def validate_text_and_image(values: dict, error: str):
    """ is validated when the type is text_and_image  """
    if 'url_image' not in values:
        raise ValueError(error.format(
            field="url_image", type=MessageEnum.TEXT_AND_IMAGE.value))


def validate_list_of_buttons(values: dict, error: str):
    """ is validated when the type is list_of_buttons  """
    if 'text_button' not in values:
        raise ValueError(error.format(
            field="text_button", type=MessageEnum.LIST_OF_BUTTONS.value))
    elif 'value_button' not in values:
        raise ValueError(error.format(
            field="value_button", type=MessageEnum.LIST_OF_BUTTONS.value))


def validate_list_of_buttons_and_image(values: dict, error: str):
    """ is validated when the type is list_of_buttons_and_image  """
    if 'text_button' not in values:
        raise ValueError(error.format(
            field="text_button",
            type=MessageEnum.LIST_OF_BUTTONS_AND_IMAGE.value))
    if 'value_button' not in values:
        raise ValueError(error.format(
            field="value_button",
            type=MessageEnum.LIST_OF_BUTTONS_AND_IMAGE.value))
    if 'url_image' not in values:
        raise ValueError(error.format(
            field="url_image",
            type=MessageEnum.LIST_OF_BUTTONS_AND_IMAGE.value))


def validate_list_of_cards(values: dict, error: str):
    """ is validated when the type is list_of_cards  """
    if 'text_carousel' not in values:
        raise ValueError(error.format(
            field="text_carousel", type=MessageEnum.LIST_OF_CARDS.value))
    if 'url_carousel' not in values:
        raise ValueError(error.format(
            field="url_carousel", type=MessageEnum.LIST_OF_CARDS.value))
    if 'text_button' not in values:
        raise ValueError(error.format(
            field="text_button", type=MessageEnum.LIST_OF_CARDS.value))
    if 'value_button' not in values:
        raise ValueError(error.format(
            field="value_button", type=MessageEnum.LIST_OF_CARDS.value))


class MessagePydantic(BaseModel):
    """ Message BaseModel """
    type: MessageEnum
    text: str
    url_image: HttpUrl = Field(
        default="", title="Url of an image")
    text_carousel: str = Field(
        default="", title="Text to go on the carousel", max_length=500)
    url_carousel: HttpUrl = Field(
        default="", title="url of an image for the carousel")
    text_button: str = Field(
        default="", title="Text to go on the button", max_length=500)
    value_button: str = Field(
        default="",
        title="value received when selecting the button",
        max_length=200
    )

    @root_validator(pre=True)
    def check_type(cls, values: dict):
        """
        it is validated that for each type of message that can be received,
        the information necessary to create the corresponding models
        is also received.
        """
        error = "{field} is required for type {type}"
        check_dict = {
            MessageEnum.TEXT_AND_IMAGE: validate_text_and_image,
            MessageEnum.LIST_OF_BUTTONS: validate_list_of_buttons,
            MessageEnum.LIST_OF_BUTTONS_AND_IMAGE: validate_list_of_buttons_and_image,
            MessageEnum.LIST_OF_CARDS: validate_list_of_cards,
        }
        check_dict[values['type']](values=values, error=error)

        return values

    class Config:
        """ Config class """
        schema_extra = {
            "example": {
                "type": "text_only",
                "text": "Any text",
                "url_image": "https://google.com/image.png",
                "text_carousel": "Any text",
                "url_carousel": "https://google.com/image.png",
                "text_button": "Any text",
                "value_button": "Any value",
            }
        }
