from fastapi import HTTPException
from typing import Literal


def SucessMessage(text: str) -> dict:
    """
    gereate a success message in the template dict
    """
    return {"detail": text}

def ErrorMessage(status: Literal[400,401,404,409,500], text: str) -> HTTPException:
    """
    generate a error message in the template HTTPException
    """
    return HTTPException(status_code=status, detail=text)

def get_text(message: dict) -> str:
    """
    get the text in a message
    """
    return message["detail"]

def generate_error_responses_from_exceptions(exceptions: list[HTTPException]) -> dict:
    """
    Gera uma estrutura de respostas de erro para FastAPI a partir de uma lista de HTTPException.

    :param exceptions: Lista de objetos HTTPException.
    :return: Dicionário formatado para o parâmetro `responses` do FastAPI.
    """
    responses = {}
    for exception in exceptions:
        status_code = exception.status_code
        detail = exception.detail

        if status_code not in responses:
            responses[status_code] = {
                "description": "Erro",
                "content": {
                    "application/json": {
                        "examples": {}
                    }
                }
            }

        example_key = detail.lower().replace(" ", "_")
        responses[status_code]["content"]["application/json"]["examples"][example_key] = {
            "summary": detail,
            "value": {"detail": detail}
        }

    return responses