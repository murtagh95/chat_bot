""" Message model """
# Tortoise
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

# Python
from enum import Enum

from app.core.models.pydantic.button_pydantic import ButtonPydantic
from app.core.models.pydantic.card_pydantic import CardPydantic
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

    async def create_button_list_in_db(self, button_list: list[ButtonPydantic]):
        """ The list of buttons related to the message is created. """
        for button in button_list:
            await Button.create(
                text=button.text,
                value=button.value,
                message_id=self.id
            )

    async def create_card_list_in_db(self, card_list: list[CardPydantic]):
        """ The list of buttons related to the message is created. """
        for card in card_list:
            new_card = await Card.create(
                text=card.text,
                url_image=card.url_image,
                message_id=self.id
            )
            await new_card.create_button_list_in_db(card.button_list_card)


message_pydantic = pydantic_model_creator(Message, name="Message")
message_pydantic_in = pydantic_model_creator(
    Message, name="MessageIn", exclude_readonly=True)
