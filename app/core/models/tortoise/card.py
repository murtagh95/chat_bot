""" Card model """
# Tortoise
from tortoise import Model, fields

# Models
from app.core.models.tortoise.button import Button
from app.core.models.pydantic.button_pydantic import (
    ButtonPydantic,
    ButtonPydanticWithId)
from app.core.models.pydantic.card_pydantic import CardPydanticWithId


class Card(Model):
    """" Card model """
    id = fields.IntField(pk=True, index=True)
    text = fields.TextField(null=False)
    url_image = fields.CharField(max_length=200, null=False)
    message = fields.ForeignKeyField(
        "models.Message", related_name="list_card")
    button_list_card: fields.ReverseRelation["Button"]

    def get_card_pydantic(self):
        list_button = []
        for button in self.button_list_card:
            list_button.append(
                ButtonPydanticWithId(
                    id=button.id,
                    text=button.text,
                    value=button.value
                )
            )

        return CardPydanticWithId(
            id=self.id,
            text=self.text,
            url_image=self.url_image,
            button_list_card=list_button
        )

    async def create_button_list_in_db(self,
                                       button_list: list[ButtonPydantic]):
        """ The list of buttons related to the card is created. """
        for button in button_list:
            await Button.create(
                text=button.text,
                value=button.value,
                card_id=self.id
            )

    async def update_button(self, index: int, new_button: ButtonPydantic):
        """  """
        old_buttons = await self.button_list_card.all()
        old_button = old_buttons[index]
        old_button = await old_button.update_from_dict(
            data=new_button.dict())
        await old_button.save(force_update=True)

    class Meta:
        """ Meta """
        table = "card"
        ordering = ("id",)
        computed = (
            "get_card_pydantic",
            "create_button_list_in_db",
            "update_button"
        )

    class PydanticMeta:
        """ Pydantic Meta """
        computed = (
            "get_card_pydantic",
            "create_button_list_in_db",
            "update_button"
        )
