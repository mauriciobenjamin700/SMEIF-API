from fastapi import (
    HTTPException,
    Response
)
from json import (
    dumps, 
    loads
)
from typing import Literal


from constants.base import ERROR_SERVER_ERROR
from schemas.base import BaseMessage


def SucessMessage(text: str) -> BaseMessage:
    """
    gereate a success message in the template dict
    """
    return BaseMessage(detail=text)







