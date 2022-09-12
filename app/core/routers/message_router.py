""" Message router """
# FastAPI
from fastapi import APIRouter, status, HTTPException

# Models
from app.core.exceptions.exceptions import RESPONSE_DICT_WITH_ERROR
from app.core.models.pydantic.card_pydantic import CardPydantic
from app.core.models.pydantic.massage_base_pydantic import MessageBase
from app.core.models.pydantic.message_pydantic import MessagePydanticIn
from app.core.models.tortoise.button import Button
from app.core.models.tortoise.card import Card
from app.core.models.tortoise.message import Message, MessageEnum
from app.core.models.tortoise.schemas.button_schemas import button_pydantic_in
from app.core.models.tortoise.schemas.message_schemas import (
    message_pydantic,
    message_pydantic_list)

router = APIRouter()


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=message_pydantic)
async def create_message(message: MessagePydanticIn):
    new_message = await Message.create(
        type=message.type, text=message.text, url=message.url)

    if message.type in [MessageEnum.LIST_OF_BUTTONS,
                        MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
        await new_message.create_button_list_in_db(message.list_button)

    elif message.type == MessageEnum.LIST_OF_CARDS:
        await new_message.create_card_list_in_db(message.list_card)
    new_message = await message_pydantic.from_tortoise_orm(new_message)
    return new_message


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=message_pydantic_list,
            description="Get all messages")
async def get_all_messages():
    return await message_pydantic_list.from_queryset(
        Message.all().prefetch_related(
            "list_button").prefetch_related('list_card')
    )


@router.get("/{message_id}",
            status_code=status.HTTP_200_OK,
            description="Get a messages",
            response_model=message_pydantic,
            responses={**RESPONSE_DICT_WITH_ERROR})
async def get_a_message(message_id: int):
    message = await Message.filter(id=message_id).prefetch_related(
        "list_button").prefetch_related('list_card').first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    return await message_pydantic.from_tortoise_orm(message)


@router.delete("/{message_id}",
               status_code=status.HTTP_200_OK,
               description="Delete a messages",
               responses={**RESPONSE_DICT_WITH_ERROR})
async def delete_message(message_id: int):
    message = await Message.filter(id=message_id).prefetch_related(
        "list_button").prefetch_related('list_card').first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    await message.delete()
    return {"detail": "Delete message"}


@router.put("/{message_id}",
            status_code=status.HTTP_200_OK,
            response_model=message_pydantic,
            description="Get a messages",
            responses={**RESPONSE_DICT_WITH_ERROR})
async def update_message(message_id: int, message: MessageBase):
    message_search = await Message.filter(id=message_id).prefetch_related(
        "list_button").prefetch_related('list_card').first()
    if not message_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    new_message = await message_search.update_from_dict(
        data=message.dict()
    )
    await new_message.save()

    return await message_pydantic.from_tortoise_orm(new_message)


@router.post("/{message_id}/button",
             status_code=status.HTTP_201_CREATED,
             response_model=message_pydantic,
             description="Add button to a message")
async def add_button(message_id: int, button: button_pydantic_in):
    message = await Message.filter(id=message_id).prefetch_related(
        "list_button").first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    if message.type in [MessageEnum.LIST_OF_BUTTONS,
                        MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
        await Button.create(
            text=button.text,
            value=button.value,
            message=message
        )
        message = await Message.filter(id=message_id).prefetch_related(
            "list_button").first()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A button can be added if the message is of type list_"
                   "of_buttons or list_of_buttons_and_image."
        )
    return await message_pydantic.from_tortoise_orm(message)


@router.put("/{message_id}/button/{button_id}",
            status_code=status.HTTP_200_OK,
            response_model=message_pydantic,
            description="Update button to a message")
async def update_button(
        message_id: int, button_id: int, button: button_pydantic_in):
    button_search = await Button.filter(
        id=button_id, message_id=message_id).first()
    if not button_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    new_button = await button_search.update_from_dict(
        data=button.dict(exclude={"message_id"})
    )
    await new_button.save()

    message = await Message.filter(id=message_id).prefetch_related(
        "list_button").prefetch_related('list_card').first()

    return await message_pydantic.from_tortoise_orm(message)


@router.post("/{message_id}/card",
             status_code=status.HTTP_201_CREATED,
             response_model=message_pydantic,
             description="Add card to a message")
async def add_card(message_id: int, card: CardPydantic):
    message = await Message.filter(id=message_id).prefetch_related(
        "list_card").first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    if message.type == MessageEnum.LIST_OF_CARDS:
        await message.create_card_list_in_db([card])
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A button can be added if the message is of type list_"
                   "of_buttons or list_of_buttons_and_image."
        )
    return await message_pydantic.from_tortoise_orm(message)


@router.put("/{message_id}/card/{card_id}",
            status_code=status.HTTP_200_OK,
            response_model=message_pydantic,
            description="Update card to a message")
async def update_card(message_id: int, card_id: int, card: CardPydantic):
    card_search = await Card.filter(id=card_id, message_id=message_id).first()
    if not card_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    card_search = await card_search.update_from_dict(
        data=card.dict(exclude={'button_list_card'})
    )
    await card_search.save()

    card_search = await Card.filter(id=card_id, message_id=message_id). \
        prefetch_related('button_list_card').first()

    if len(card.button_list_card) == len(card_search.button_list_card):
        for i in range(len(card.button_list_card)):
            await card_search.update_button(
                index=i,
                new_button=card.button_list_card[i])

    elif len(card.button_list_card) > len(card_search.button_list_card):
        for i in range(len(card.button_list_card)):
            try:
                await card_search.update_button(
                    index=i,
                    new_button=card.button_list_card[i])
            except IndexError:
                await Button.create(
                    text=card.button_list_card[i].text,
                    value=card.button_list_card[i].value,
                    card=card_search
                )
    else:
        for i in range(len(card_search.button_list_card)):
            try:
                await card_search.update_button(
                    index=i,
                    new_button=card.button_list_card[i])
            except IndexError:
                old_buttons = await card_search.button_list_card.all().order_by(
                    'id')
                await old_buttons[i].delete()

    message = await Message.filter(id=message_id).prefetch_related(
        "list_button").prefetch_related('list_card').first()

    return await message_pydantic.from_tortoise_orm(message)
