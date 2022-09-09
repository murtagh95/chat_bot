""" Message router """
# FastAPI
from fastapi import APIRouter, status, HTTPException

# Models
from app.core.exceptions.exceptions import RESPONSE_DICT_WITH_ERROR
from app.core.models.pydantic.button_pydantic import ButtonPydanticWithId
from app.core.models.pydantic.card_pydantic import CardPydantic
from app.core.models.pydantic.massage_base_pydantic import MessageBase
from app.core.models.pydantic.message_pydantic import (
    MessagePydanticIn,
    MessagePydanticOut)
from app.core.models.tortoise.button import Button, button_pydantic_in
from app.core.models.tortoise.card import Card
from app.core.models.tortoise.message import (
    Message,
    MessageEnum,
    message_pydantic
)

router = APIRouter()


async def get_message_in_pydantic(message: Message) -> MessagePydanticOut:
    if message.type in \
            [MessageEnum.LIST_OF_BUTTONS,
             MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
        buttons_messages = await message.button_message.all()
        list_button = [
            ButtonPydanticWithId(id=b.id, text=b.text, value=b.value) for b in
            buttons_messages
        ]
        return MessagePydanticOut(
            id=message.id,
            type=message.type,
            text=message.text,
            url=message.url or None,
            list_button=list_button
        )

    elif message.type == MessageEnum.LIST_OF_CARDS:
        card_messages = await message.card_message.all().prefetch_related(
            "button_list_card"
        )
        return MessagePydanticOut(
            id=message.id,
            type=message.type,
            text=message.text,
            list_card=[c.get_card_pydantic() for c in card_messages]
        )
    else:
        message_pydantic_model = await message_pydantic.from_tortoise_orm(
            message)
        return MessagePydanticOut(**message_pydantic_model.dict())


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=MessagePydanticOut)
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
            response_model=list[MessagePydanticOut],
            description="Get all messages")
async def get_all_messages():
    messages = await Message.all().prefetch_related(
        "button_message").prefetch_related('card_message')
    list_message: list[MessagePydanticOut] = []
    for message in messages:
        list_message.append(
            await get_message_in_pydantic(message)
        )

    return list_message


@router.get("/{message_id}",
            status_code=status.HTTP_200_OK,
            response_model=MessagePydanticOut,
            description="Get a messages",
            responses={**RESPONSE_DICT_WITH_ERROR})
async def get_a_message(message_id: int):
    message = await Message.filter(id=message_id).prefetch_related(
        "button_message").prefetch_related('card_message').first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    return await get_message_in_pydantic(message)


@router.delete("/{message_id}",
               status_code=status.HTTP_200_OK,
               description="Delete a messages",
               responses={**RESPONSE_DICT_WITH_ERROR})
async def delete_message(message_id: int):
    message = await Message.filter(id=message_id).prefetch_related(
        "button_message").prefetch_related('card_message').first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    await message.delete()
    return {"detail": "Delete message"}


@router.put("/{message_id}",
            status_code=status.HTTP_200_OK,
            description="Get a messages",
            responses={**RESPONSE_DICT_WITH_ERROR})
async def update_message(message_id: int, message: MessageBase):
    message_search = await Message.filter(id=message_id).prefetch_related(
        "button_message").prefetch_related('card_message').first()
    if not message_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    new_message = await message_search.update_from_dict(
        data=message.dict()
    )
    await new_message.save()

    return await get_message_in_pydantic(new_message)


@router.post("/{message_id}/button",
             status_code=status.HTTP_201_CREATED,
             response_model=MessagePydanticOut,
             description="Add button to a message")
async def add_button(message_id: int, button: button_pydantic_in):
    message = await Message.filter(id=message_id).prefetch_related(
        "button_message").first()
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
            "button_message").first()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A button can be added if the message is of type list_"
                   "of_buttons or list_of_buttons_and_image."
        )
    return await get_message_in_pydantic(message)


@router.put("/{message_id}/button/{button_id}",
            status_code=status.HTTP_201_CREATED,
            response_model=MessagePydanticOut,
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
        data=button.dict()
    )
    await new_button.save()

    message = await Message.filter(id=message_id).prefetch_related(
        "button_message").prefetch_related('card_message').first()

    return await get_message_in_pydantic(message)


@router.post("/{message_id}/card",
             status_code=status.HTTP_201_CREATED,
             response_model=MessagePydanticOut,
             description="Add card to a message")
async def add_card(message_id: int, card: CardPydantic):
    message = await Message.filter(id=message_id).prefetch_related(
        "card_message").first()
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
    return await get_message_in_pydantic(message)


@router.put("/{message_id}/card/{card_id}",
            status_code=status.HTTP_201_CREATED,
            response_model=MessagePydanticOut,
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
        "button_message").prefetch_related('card_message').first()

    return await get_message_in_pydantic(message)
