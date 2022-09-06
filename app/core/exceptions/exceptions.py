"""API Exceptions"""
from pydantic import BaseModel


class HTTPError(BaseModel):
    """ HTTP error """
    detail: str

    class Config:
        """" Config class """
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


class ValidationError(BaseModel):
    loc: list
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """ Validation Error """
    detail: list[ValidationError]

    class Config:
        """" Config class """
        schema_extra = {
            "example": {
                "detail": [
                    {
                        "loc": [
                            "string",
                            0
                        ],
                        "msg": "string",
                        "type": "string"
                    }
                ]
            }
        }


RESPONSE_DICT_WITH_ERROR = {
    404: {
        "model": HTTPError,
        "description": "This endpoint always raises an error",
    },
    422: {
        "model": ValidationError,
        "description": "Validation Error"
    }
}
