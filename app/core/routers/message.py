""" Message router """
# FastAPI
from fastapi import APIRouter, status

# Models
from app.core.models.pydantic.message_list_of_buttons import \
    MessageListOfButtons
from app.core.models.pydantic.message_pydantic import MessagePydantic
from app.core.models.pydantic.message_list_of_cards import MessageListOfCards
from app.core.models.tortoise.button import Button
from app.core.models.tortoise.card import Card
from app.core.models.tortoise.message import (
    Message,
    MessageEnum,
    message_pydantic
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_message(message: MessagePydantic):
    new_message = await Message.create(
        type=message.type, text=message.text, url=message.url)

    if message.type in [MessageEnum.LIST_OF_BUTTONS,
                        MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
        await Button.create(
            text=message.text_button,
            value=message.value_button,
            message=new_message
        )

    elif message.type == MessageEnum.LIST_OF_CARDS:
        card = await Card.create(
            text=message.text_card,
            url_image=message.url_card,
            message=new_message
        )
        await Button.create(
            text=message.text_button,
            value=message.value_button,
            card=card
        )
    # new_message = await Message.filter(id=new_message.id).prefetch_related(
    #     "message_image").first()
    new_message = await message_pydantic.from_tortoise_orm(new_message)
    return new_message


@router.get("/",
            status_code=status.HTTP_200_OK,
            description="Get all messages")
async def get_messages():
    messages = await Message.all().prefetch_related(
        "button_message").prefetch_related('card_message')
    list_message = []
    for message in messages:
        if message.type in \
                [MessageEnum.LIST_OF_BUTTONS,
                 MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
            buttons_messages = await message.button_message.all()
            list_message.append(
                MessageListOfButtons(
                    id=message.id,
                    type=message.type,
                    text=message.text,
                    url=message.url or None,
                    list_button=[b for b in buttons_messages]
                )
            )
        elif message.type == MessageEnum.LIST_OF_CARDS:
            card_messages = await message.card_message.all().prefetch_related(
                "button_list_card"
            )
            list_message.append(
                MessageListOfCards(
                    id=message.id,
                    type=message.type,
                    text=message.text,
                    list_card=[c.get_card_pydantic() for c in card_messages]
                )
            )
        else:
            list_message.append(message)

    return list_message
