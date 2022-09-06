""" Card model """
# Tortoise
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from app.core.models.pydantic.button_pydantic import ButtonPydantic
from app.core.models.pydantic.card_pydantic import CardPydantic
# Models
from app.core.models.tortoise.button import Button


class Card(Model):
    """" Card model """
    id = fields.IntField(pk=True, index=True)
    text = fields.TextField(null=False)
    url_image = fields.CharField(max_length=200, null=False)
    message = fields.ForeignKeyField(
        "models.Message", related_name="card_message")
    button_list_card: fields.ReverseRelation["Button"]

    def get_card_pydantic(self):
        list_button = []
        for button in self.button_list_card:
            list_button.append(
                ButtonPydantic(
                    text=button.text,
                    value=button.value
                )
            )

        return CardPydantic(
            text=self.text,
            url_image=self.url_image,
            button_list_card=list_button
        )

    class Meta:
        """ Meta """
        table = "card"

    class PydanticMeta:
        """ Pydantic Meta """
        computed = ("get_card_pydantic",)


card_pydantic = pydantic_model_creator(Card, name="Card")
card_pydantic_in = pydantic_model_creator(
    Card, name="CardIn", exclude_readonly=True)
