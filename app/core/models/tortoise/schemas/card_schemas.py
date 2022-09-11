# Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

# Models
from app.core.models.tortoise.card import Card


card_pydantic = pydantic_model_creator(Card, name="Card")
card_pydantic_in = pydantic_model_creator(
    Card, name="CardIn", exclude_readonly=True)
