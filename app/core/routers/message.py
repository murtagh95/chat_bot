""" Message router """
# FastAPI
from fastapi import APIRouter, status

# Models
from app.core.models.pydantic.message_pydantic import MessagePydantic
from app.core.models.tortoise.button import Button
from app.core.models.tortoise.carousel import Carousel
from app.core.models.tortoise.image import Image
from app.core.models.tortoise.message import (
    Message,
    MessageEnum,
    message_pydantic
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_message(message: MessagePydantic):
    new_message = await Message.create(type=message.type, text=message.text)
    if message.type in \
            [MessageEnum.TEXT_AND_IMAGE, MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
        await Image.create(url=message.url_image, message=new_message)

    if message.type in [MessageEnum.LIST_OF_BUTTONS,
                        MessageEnum.LIST_OF_BUTTONS_AND_IMAGE]:
        await Button.create(
            text=message.text_button,
            value=message.value_button,
            message=new_message
        )

    elif message.type == MessageEnum.LIST_OF_CARDS:
        carousel = await Carousel.create(
            text=message.text_carousel,
            url_image=message.url_carousel,
            message=new_message
        )
        await Button.create(
            text=message.text_button,
            value=message.value_button,
            carousel=carousel
        )

    new_message = await message_pydantic.from_tortoise_orm(new_message)
    return new_message
