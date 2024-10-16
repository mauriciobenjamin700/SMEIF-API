from fastapi import HTTPException
from typing import Literal


def gererate_sucess_message(text: str) -> dict:
    """
    gereate a success message in the template dict
    """
    return {"detail": text}

def generate_error_message(status: Literal[400,401,404,409,500], text: str) -> HTTPException:
    """
    generate a error message in the template HTTPException
    """
    return HTTPException(status_code=status, detail=text)

def get_text(message: dict) -> str:
    """
    get the text in a message
    """
    return message["detail"]

def get_error_data(error: HTTPException) -> dict:
    """
    return:
        tuple: status_code, detail
    """
    return error.value.status_code, error.value.detail