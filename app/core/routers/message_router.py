""" Message router """
# FastAPI
from fastapi import APIRouter, status, HTTPException

# Models
from app.core.exceptions.exceptions import RESPONSE_DICT_WITH_ERROR
from app.core.models.pydantic.button_pydantic import ButtonPydantic
from app.core.models.pydantic.message_list_of_buttons import \
    MessageListOfButtons
from app.core.models.pydantic.message_pydantic import MessagePydanticIn, \
    MessagePydanticOut
from app.core.models.pydantic.message_list_of_cards import MessageListOfCards
from app.core.models.tortoise.button import Button, button_pydantic_in
from app.core.models.tortoise.message import (
    Message,
    MessageEnum,
    message_pydantic
)

router = APIRouter()


async def get_message_in_pydantic(message: Message) \
        -> MessageListOfButtons | MessageListOfCards | Message:
    if message.type in \
            [MessageEnum.LIST_OF_BUTTONS,
             MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
        buttons_messages = await message.button_message.all()
        list_button = [
            ButtonPydantic(text=b.text, value=b.value) for b in buttons_messages
        ]
        return MessageListOfButtons(
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
        return MessageListOfCards(
            id=message.id,
            type=message.type,
            text=message.text,
            list_card=[c.get_card_pydantic() for c in card_messages]
        )
    else:
        return message


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
    list_message = []
    for message in messages:
        list_message.append(
            await get_message_in_pydantic(message)
        )

    return list_message


RESPONSE_GET_A_MESSAGE = {
    **RESPONSE_DICT_WITH_ERROR,
    200: {
        "model": MessageListOfButtons | MessageListOfCards | message_pydantic
    }
}


@router.get("/{message_id}",
            status_code=status.HTTP_200_OK,
            description="Get a messages",
            responses=RESPONSE_GET_A_MESSAGE)
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
            responses=RESPONSE_GET_A_MESSAGE)
async def update_message(message_id: int, message: MessagePydanticIn):
    message = await Message.filter(id=message_id).prefetch_related(
        "button_message").prefetch_related('card_message').first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    return await get_message_in_pydantic(message)


@router.post("/{message_id}/button",
             status_code=status.HTTP_201_CREATED,
             response_model=MessageListOfButtons,
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
