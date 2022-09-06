""" Business model """
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Business(Model):
    """" Business model """
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=20, null=False, unique=True)
    city = fields.CharField(max_length=100, null=False, default="Unspecified")
    region = fields.CharField(max_length=100, null=False, default="Unspecified")
    description = fields.TextField(null=True)
    logo = fields.CharField(max_length=200, null=False, default="default.png")
    owner = fields.ForeignKeyField("models.User", related_name="business")

    class Meta:
        """ Meta """
        table = "business"


business_pydantic = pydantic_model_creator(Business, name="Business")
business_pydantic_in = pydantic_model_creator(
    Business, name="BusinessIn", exclude_readonly=True)
