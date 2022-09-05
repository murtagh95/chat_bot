""" Way model """
# Tortoise
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Way(Model):
    """" Way model """
    id = fields.IntField(pk=True, index=True)
    is_first = fields.BooleanField(default=False)
    condition = fields.CharField(max_length=200, null=False)
    message = fields.ForeignKeyField(
        "models.Message", related_name="message_way")
    related_way = fields.ForeignKeyField(
        "models.Way",
        related_name="way"
    )

    class Meta:
        """ Meta """
        table = "way"


way_pydantic = pydantic_model_creator(Way, name="Way")
way_pydantic_in = pydantic_model_creator(
    Way, name="WayIn", exclude_readonly=True)
