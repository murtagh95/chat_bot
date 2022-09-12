""" Way model """
# Tortoise
from tortoise import Model, fields


class Way(Model):
    """ Way model """
    id = fields.IntField(pk=True, index=True)
    is_first = fields.BooleanField(default=False)
    condition = fields.CharField(max_length=200, null=True)
    message = fields.ForeignKeyField(
        "models.Message", related_name="message_way")
    related_way = fields.ForeignKeyField(
        "models.Way",
        related_name="way",
        null=True
    )

    class Meta:
        """ Meta """
        table = "way"
        ordering = ("id",)

    # class PydanticMeta:
    #     exclude = (
    #         "message.list_button",
    #         "message.list_card"
    #     )
