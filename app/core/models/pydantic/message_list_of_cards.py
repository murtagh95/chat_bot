# Models
from app.core.models.pydantic.card_pydantic import CardPydantic
from app.core.models.pydantic.massage_base_pydantic import MessageBaseWithID


class MessageListOfCards(MessageBaseWithID):
    list_card: list[CardPydantic]
