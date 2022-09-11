""" Button model """
# Tortoise
from tortoise import Model, fields


class Button(Model):
    """" Button model """
    id = fields.IntField(pk=True, index=True)
    text = fields.TextField(null=False)
    value = fields.CharField(max_length=200, null=False)
    message = fields.ForeignKeyField(
        "models.Message",
        related_name="list_button",
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
        ordering = ("id",)
