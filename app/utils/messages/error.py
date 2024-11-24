"""
## Mensagens de Erro

### Funcs

- BadRequest
- Unauthorized
- Forbidden
- NotFound
- Conflict
- UnprocessableEntity
- Server

"""
from fastapi import HTTPException


from constants.base import ERROR_SERVER_ERROR


def BadRequest(errors: str) -> HTTPException:
    return HTTPException(status_code=400, detail=errors)


def Unauthorized(detail:str) -> HTTPException:
    return HTTPException(status_code=401, detail=detail)


def Forbidden(detail:str) -> HTTPException:
    return HTTPException(status_code=403, detail=detail)


def NotFound(detail:str) -> HTTPException:
    return HTTPException(status_code=404, detail=detail)


def Conflict(detail:str) -> HTTPException:
    return HTTPException(status_code=409, detail=detail)


def UnprocessableEntity(errors: str) -> HTTPException:
    return HTTPException(status_code=422, detail=errors)


def Server(error: Exception) -> HTTPException:
    return HTTPException(status_code=500, detail=f"{ERROR_SERVER_ERROR}{error}")