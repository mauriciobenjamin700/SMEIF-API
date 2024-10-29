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


def SucessMessage(text: str) -> dict:
    """
    gereate a success message in the template dict
    """
    return BaseMessage(detail=text)

def ErrorMessage(status: Literal[400,401,404,409,500], text: str) -> HTTPException:
    """
    generate a error message in the template HTTPException
    """
    return HTTPException(status_code=status, detail=text)


def ConflitErrorMessage(detail:str) -> HTTPException:
    return HTTPException(status_code=409, detail=detail)


def UnauthorizedErrorMessage(detail:str) -> HTTPException:
    return HTTPException(status_code=401, detail=detail)


def NotFoundErrorMessage(detail:str) -> HTTPException:
    return HTTPException(status_code=404, detail=detail)


def ValidationErrorMessage(errors: dict) -> HTTPException:
    """
    generate a validation error message in the template HTTPException
    """
    return HTTPException(status_code=400, detail=errors)


def ServerError(error: Exception) -> HTTPException:
    """
    generate a server error message in the template HTTPException
    """
    return HTTPException(status_code=500, detail=f"{ERROR_SERVER_ERROR}{error}")





def generate_response(status_code: Literal[200,400,401,404,409,500], detail: str ) -> Response:
    """
    Generate a response object for FastAPI.
    """
    content = dumps({"detail": detail})
    response =  Response(status_code=status_code, content=content, media_type="application/json")
    return response

def generate_responses_documentation(responses_list: list[Response]) -> dict:
    """
    Gera uma estrutura de respostas para FastAPI a partir de uma lista de objetos Response.

    :param responses_list: Lista de objetos Response.
    :return: Dicionário formatado para o parâmetro `responses` do FastAPI.
    """
    responses = {}
    for response in responses_list:
        status_code = response.status_code
        content = response.body if response.body else {"detail": "Success"}
        #print("linha 56", content)
        if status_code not in responses:
            responses[status_code] = {
                "description": "Erro" if status_code >= 400 else "Sucesso",
                "content": {
                    "application/json": {
                        "examples": {}
                    }
                }
            }

        
        dict_content = loads(content.decode("utf-8"))
        detail = dict_content.get("detail", "Success")
        example_key = detail.lower().replace(" ", "_")
        responses[status_code]["content"]["application/json"]["examples"][example_key] = {
            "summary": detail,
            "value": dict_content
        }

    return responses