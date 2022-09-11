# Tortoise
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    pydantic_queryset_creator)

# Models
from app.core.models.tortoise.message import Message


message_pydantic = pydantic_model_creator(Message, name="Message")
message_pydantic_in = pydantic_model_creator(
    Message, name="MessageIn", exclude_readonly=True)
message_pydantic_list = pydantic_queryset_creator(Message)
