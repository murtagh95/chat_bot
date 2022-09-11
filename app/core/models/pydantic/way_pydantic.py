""" New message base model """
# Utils
from pydantic import root_validator, BaseModel, Field

# Models
from app.core.models.tortoise.message import Message
from app.core.models.tortoise.way import Way


class WayPydanticIn(BaseModel):
    """ Way BaseModel """
    is_first: bool = False
    condition: str = Field(title="Condition to enter the way", max_length=200)
    message_id: int
    related_way_id: int = None

    async def message_exist(self):
        """ Verify that the message exists """
        if not await Message.filter(id=self.message_id).exists():
            raise ValueError('The message does not match a record in '
                             'the database.')

    async def related_way_exist(self):
        """ Verify that the related way exists """
        way_exists = await Way.filter(id=self.related_way_id).exists()
        if self.related_way_id is not None and not way_exists:
            raise ValueError('The related_way does not match a record in '
                             'the database.')

    @root_validator(pre=False)
    def check_type(cls, values: dict):
        """
        Check that if the is_first field is set to true, a related_way
        is not sent.
        """
        if values.get('is_first', None) is True and \
                values.get('related_way_id', None) is not None:
            raise ValueError('If it is the first way, it should not have a '
                             'related way.')
        if values.get('is_first', None) is False and \
                values.get('related_way_id', None) is None:
            raise ValueError('If it is not the first way, it is required '
                             'that it has a related way.')
        return values
