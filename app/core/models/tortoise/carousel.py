""" Carousel model """
# Tortoise
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Carousel(Model):
    """" Carousel model """
    id = fields.IntField(pk=True, index=True)
    text = fields.TextField(null=False)
    url_image = fields.CharField(max_length=200, null=False)
    message = fields.ForeignKeyField(
        "models.Message", related_name="message_carousel")

    class Meta:
        """ Meta """
        table = "carousel"


carousel_pydantic = pydantic_model_creator(Carousel, name="Carousel")
carousel_pydantic_in = pydantic_model_creator(
    Carousel, name="CarouselIn", exclude_readonly=True)
