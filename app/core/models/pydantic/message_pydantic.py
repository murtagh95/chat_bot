""" New message base model """
# Utils
from pydantic import root_validator

# Models
from app.core.models.tortoise.message import MessageEnum
from app.core.models.pydantic.massage_base_pydantic import (
    MessageBase,
    MessageBaseWithID)
from app.core.models.pydantic.button_pydantic import ButtonPydantic
from app.core.models.pydantic.card_pydantic import CardPydantic


ERROR_REQUIRED_FIELD = "{field} is required for type {type}"
ERROR_FIELD_NOT_REQUIRED = "{field} should not be sent when it is of type " \
                           "{type}"


def validate_list_value_is_empty(
        list_value: list | None,
        message_type: MessageEnum,
        field: str) -> None:
    """
    It is verified that a list of values is empty or null, if it is not,
    an error will be returned.

    @raise ValueError: If the list is not empty
    """
    if list_value is not None and len(list_value):
        raise ValueError(ERROR_FIELD_NOT_REQUIRED.format(
            field=field, type=message_type.value))


def validate_text_only(values: dict) -> None:
    """ is validated when the type is text_only  """
    validate_list_value_is_empty(list_value=values.get("list_button", None),
                                 message_type=MessageEnum.TEXT_ONLY,
                                 field="list_button")
    validate_list_value_is_empty(list_value=values.get("list_card", None),
                                 message_type=MessageEnum.TEXT_ONLY,
                                 field="list_card")


def validate_text_and_image(values: dict):
    """ is validated when the type is text_and_image  """
    if "url" not in values or values["url"] == "":
        raise ValueError(ERROR_REQUIRED_FIELD.format(
            field="url", type=MessageEnum.TEXT_AND_IMAGE.value))

    validate_list_value_is_empty(list_value=values.get("list_button", None),
                                 message_type=MessageEnum.TEXT_AND_IMAGE,
                                 field="list_button")
    validate_list_value_is_empty(list_value=values.get("list_card", None),
                                 message_type=MessageEnum.TEXT_AND_IMAGE,
                                 field="list_card")


def validate_list_of_buttons(values: dict):
    """
    Is validated when the type is list_of_buttons and
    list_of_buttons_and_image.
    """
    list_button = values.get("list_button", None)
    if list_button is None or len(list_button) == 0:
        raise ValueError(ERROR_REQUIRED_FIELD.format(
            field="list_button", type=MessageEnum.LIST_OF_BUTTONS.value))

    validate_list_value_is_empty(list_value=values.get("list_card", None),
                                 message_type=MessageEnum.LIST_OF_BUTTONS,
                                 field="list_card")


def validate_list_of_cards(values: dict):
    """ is validated when the type is list_of_cards  """
    list_card = values.get("list_card", None)
    if list_card is None or len(list_card) == 0:
        raise ValueError(ERROR_REQUIRED_FIELD.format(
            field="list_card", type=MessageEnum.LIST_OF_CARDS.value))

    validate_list_value_is_empty(list_value=values.get("list_button", None),
                                 message_type=MessageEnum.LIST_OF_CARDS,
                                 field="list_button")


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


class MessagePydanticIn(MessageBase):
    """ Message BaseModel """
    list_button: list[ButtonPydantic] = []
    list_card: list[CardPydantic] = []

    @root_validator(pre=False)
    def check_type(cls, values: dict):
        """
        it is validated that for each type of message that can be received,
        the information necessary to create the corresponding models
        is also received.
        """
        check_dict = {
            MessageEnum.TEXT_ONLY: validate_text_only,
            MessageEnum.TEXT_AND_IMAGE: validate_text_and_image,
            MessageEnum.LIST_OF_BUTTONS: validate_list_of_buttons,
            MessageEnum.LIST_OF_BUTTONS_AND_IMAGE: validate_list_of_buttons,
            MessageEnum.LIST_OF_CARDS: validate_list_of_cards,
        }
        if "type" not in values:
            # If the guy doesn't come I let pydantic return an error.
            return values
        validate_url_according_type(values=values)
        check_dict[values["type"]](values=values)

        return values

    class Config:
        """ Config class """
        schema_extra = {
            "example": {
                "type": "text_only | text_and_image | list_of_buttons | "
                        "list_of_buttons_and_image | list_of_cards",
                "text": "Any text",
                "url": "https://google.com/image.png",
                "list_button": [
                    {
                        "text": "Any text",
                        "value": "Any"
                    }
                ],
                "list_card": [
                    {
                        "text": "Any text",
                        "url_image": "https://google.com/image.png",
                        "button_list_card": [
                            {
                                "text": "Any text",
                                "value": "Any"
                            }
                        ]
                    }
                ]
            }
        }


class MessagePydanticOut(MessageBaseWithID):
    """ Message BaseModel """
    list_button: list[ButtonPydantic] = []
    list_card: list[CardPydantic] = []
