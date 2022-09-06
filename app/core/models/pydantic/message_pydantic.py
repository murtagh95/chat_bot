""" New message base model """
# Utils
from pydantic import Field, HttpUrl, root_validator

# Models
from app.core.models.tortoise.message import MessageEnum
from app.core.models.pydantic.massage_base_pydantic import MessageBase


def validate_text_only(values: dict, error: str):
    """ is validated when the type is text_only  """
    if 'url' in values:
        raise ValueError(
            "url should not be sent when it is of type text_only")


def validate_text_and_image(values: dict, error: str):
    """ is validated when the type is text_and_image  """
    if "url" not in values or values["url"] == "":
        raise ValueError(error.format(
            field="url", type=MessageEnum.TEXT_AND_IMAGE.value))


def validate_list_of_buttons(values: dict, error: str):
    """ is validated when the type is list_of_buttons  """
    if 'text_button' not in values:
        raise ValueError(error.format(
            field="text_button", type=MessageEnum.LIST_OF_BUTTONS.value))
    elif 'value_button' not in values:
        raise ValueError(error.format(
            field="value_button", type=MessageEnum.LIST_OF_BUTTONS.value))
    if "url" in values and values["url"] is not None:
        raise ValueError(
            "url should not be sent when it is of type list_of_buttons")


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
    if "url" not in values or values["url"] == "":
        raise ValueError(error.format(
            field="url",
            type=MessageEnum.LIST_OF_BUTTONS_AND_IMAGE.value))


def validate_list_of_cards(values: dict, error: str):
    """ is validated when the type is list_of_cards  """
    if 'text_card' not in values:
        raise ValueError(error.format(
            field="text_card", type=MessageEnum.LIST_OF_CARDS.value))
    if 'url_card' not in values:
        raise ValueError(error.format(
            field="url_card", type=MessageEnum.LIST_OF_CARDS.value))
    if 'text_button' not in values:
        raise ValueError(error.format(
            field="text_button", type=MessageEnum.LIST_OF_CARDS.value))
    if 'value_button' not in values:
        raise ValueError(error.format(
            field="value_button", type=MessageEnum.LIST_OF_CARDS.value))
    if "url" in values and values["url"] is not None:
        raise ValueError(
            "url should not be sent when it is of type list_of_cards")


class MessagePydantic(MessageBase):
    """ Message BaseModel """
    text_card: str = Field(
        default="", title="Text to go on the card", max_length=500)
    url_card: HttpUrl = Field(
        default="", title="url of an image for the card")
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
            MessageEnum.TEXT_ONLY: validate_text_only,
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
                "url": "https://google.com/image.png",
                "text_card": "Any text",
                "url_card": "https://google.com/image.png",
                "text_button": "Any text",
                "value_button": "Any value",
            }
        }
