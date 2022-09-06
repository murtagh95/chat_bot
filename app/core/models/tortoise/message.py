""" Message model """
# Tortoise
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

# Python
from enum import Enum

# Models
from app.core.models.tortoise.button import Button
from app.core.models.tortoise.card import Card


class MessageEnum(str, Enum):
    """ Enum of the different types of messages that can exist """
    TEXT_ONLY = "text_only"
    TEXT_AND_IMAGE = "text_and_image"
    LIST_OF_BUTTONS = "list_of_buttons"
    LIST_OF_BUTTONS_AND_IMAGE = "list_of_buttons_and_image"
    LIST_OF_CARDS = "list_of_cards"


class Message(Model):
    """" Message model """
    id = fields.IntField(pk=True, index=True)
    type: MessageEnum = fields.CharEnumField(
        MessageEnum,
        default=MessageEnum.TEXT_ONLY
    )
    text = fields.TextField(null=False)
    url = fields.CharField(max_length=200, null=True, default='')
    button_message: fields.ReverseRelation["Button"]
    card_message: fields.ReverseRelation["Card"]

    class Meta:
        """ Meta """
        table = "message"


message_pydantic = pydantic_model_creator(Message, name="Message")
message_pydantic_in = pydantic_model_creator(
    Message, name="MessageIn", exclude_readonly=True)
