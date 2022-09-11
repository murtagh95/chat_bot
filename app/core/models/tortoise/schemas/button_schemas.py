# Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

# Models
from app.core.models.tortoise.button import Button


button_pydantic = pydantic_model_creator(Button, name="Button")
button_pydantic_in = pydantic_model_creator(
    Button, name="ButtonIn", exclude_readonly=True)
