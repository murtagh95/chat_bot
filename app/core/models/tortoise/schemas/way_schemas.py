# Tortoise
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    pydantic_queryset_creator)

# Models
from app.core.models.tortoise.way import Way


way_pydantic = pydantic_model_creator(Way, name="Way")
way_pydantic_in = pydantic_model_creator(
    Way, name="WayIn", exclude_readonly=True)
way_pydantic_list = pydantic_queryset_creator(Way)
