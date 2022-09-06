""" Product model """
from datetime import datetime
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Product(Model):
    """ Product model """
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=100, null=False, index=True)
    category = fields.CharField(max_length=30, index=True)
    original_prince = fields.DecimalField(max_digits=12, decimal_places=2)
    new_prince = fields.DecimalField(max_digits=12, decimal_places=2)
    percentage_discount = fields.DecimalField(max_digits=2, decimal_places=2)
    offer_expiration_data = fields.DateField(default=datetime.utcnow())
    image = fields.CharField(
        max_length=200, null=False, default="productDefault.png")
    business = fields.ForeignKeyField(
        "models.Business", related_name="products")

    class Meta:
        """ Meta """
        table = 'product'


product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydantic_in = pydantic_model_creator(
    Product, name="ProductIn", exclude=("percentage_discount", "id"))
