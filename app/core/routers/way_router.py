""" Message router """
# FastAPI
from fastapi import APIRouter, status, HTTPException

# Models
from app.core.models.pydantic.way_pydantic import WayPydanticIn
from app.core.models.tortoise.schemas.way_schemas import (
    way_pydantic,
    way_pydantic_list)
from app.core.models.tortoise.way import Way

# Utils
from app.core.exceptions.exceptions import RESPONSE_DICT_WITH_ERROR

router = APIRouter()


@router.post("/",
             responses={**RESPONSE_DICT_WITH_ERROR},
             status_code=status.HTTP_201_CREATED)
async def create_way(way: WayPydanticIn):
    try:
        await way.related_way_exist() and way.message_exist()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.__str__()
        )
    new_way = await Way.create(**way.dict())

    return await way_pydantic.from_tortoise_orm(new_way)


@router.get("/",
            response_model=way_pydantic_list,
            status_code=status.HTTP_200_OK)
async def get_all_ways():
    return await way_pydantic_list.from_queryset(
        Way.all()
    )


@router.get("/{way_id}",
            response_model=way_pydantic,
            status_code=status.HTTP_200_OK)
async def get_a_way(way_id: int):
    way = await Way.filter(id=way_id).first()
    if not way:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Way not found"
        )

    return await way_pydantic.from_tortoise_orm(way)


@router.delete("/{way_id}",
               status_code=status.HTTP_200_OK)
async def delete_way(way_id: int):
    way = await Way.filter(id=way_id).first()
    if not way:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Way not found"
        )

    await way.delete()
    return {"detail": "Delete way"}
