""" Message with type list of buttons """
# Models
from app.core.models.pydantic.button_pydantic import ButtonPydantic
from app.core.models.pydantic.massage_base_pydantic import MessageBaseWithID


class MessageListOfButtons(MessageBaseWithID):
    """ Message list of buttons and Image """
    list_button: list[ButtonPydantic]
