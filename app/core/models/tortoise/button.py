""" Button model """
# Tortoise
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Button(Model):
    """" Button model """
    id = fields.IntField(pk=True, index=True)
    text = fields.TextField(null=False)
    value = fields.CharField(max_length=200, null=False)
    message = fields.ForeignKeyField(
        "models.Message",
        related_name="button_message",
        null=True
    )
    card = fields.ForeignKeyField(
        "models.Card",
        related_name="button_list_card",
        null=True
    )

    class Meta:
        """ Meta """
        table = "button"


button_pydantic = pydantic_model_creator(Button, name="Button")
button_pydantic_in = pydantic_model_creator(
    Button, name="ButtonIn", exclude_readonly=True)
