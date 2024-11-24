from schemas.base import BaseMessage


def Success(detail: str) -> BaseMessage:
    return BaseMessage(detail=detail)
