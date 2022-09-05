""" Image model """
# Tortoise
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Image(Model):
    """" Image model """
    id = fields.IntField(pk=True, index=True)
    url = fields.CharField(max_length=200, null=False)
    message = fields.ForeignKeyField(
        "models.Message", related_name="message_image")

    class Meta:
        """ Meta """
        table = "image"


image_pydantic = pydantic_model_creator(Image, name="Image")
image_pydantic_in = pydantic_model_creator(
    Image, name="ImageIn", exclude_readonly=True)
