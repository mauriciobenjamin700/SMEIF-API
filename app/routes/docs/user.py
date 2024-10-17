from fastapi import Response


from constants.base import ERROR_SERVER_ERROR
from constants.user import (
    ERROR_CPF_ALREADY_EXISTS, 
    ERROR_EMAIL_ALREADY_EXISTS,
    ERROR_NOT_FOUND_USER,
    ERROR_NOT_ID, 
    ERROR_PHONE_ALREADY_EXISTS, 
    MESSAGE_ADD_SUCESS
)

USER_REQUEST_EXAMPLE =         {
            "cpf": "123.456.789-00",
            "name": "John Doe",
            "phone": "(00) 90000-0000",
            "phone_optional": "(00) 9000-0001",
            "email": " jhon.doe@example.com",
            "password": '123',
            "level": 1
        }  
USER_RESPONSE_EXAMPLE = {
    "cpf": "123.456.789-00",
    "name": "John Doe",
    "phone": "(00) 90000-0000",
    "phone_optional": "(00) 9000-0001",
    "email": "john@example",
    "level": 1
}

from utils.messages import generate_response, generate_responses_documentation


ADD_RESPONSE_DESCRIPTION = f"""

- Exemplo de resposta:

            "detail": "{MESSAGE_ADD_SUCESS}"
        

"""

ADD_DESCRIPTION = """
Adiciona um novo usuário ao banco de dados.
             
- Exemplo de requisição:
             
        {
            "cpf": "123.456.789-00",
            "name": "John Doe",
            "phone": "(00) 90000-0000",
            "phone_optional": "(00) 9000-0001",
            "email": " jhon.doe@example.com",
            "password": '123',
            "level": 1
        }         
""" + ADD_RESPONSE_DESCRIPTION

ADD_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_ADD_SUCESS),
        generate_response(409, ERROR_CPF_ALREADY_EXISTS),
        generate_response(409, ERROR_PHONE_ALREADY_EXISTS),
        generate_response(409, ERROR_EMAIL_ALREADY_EXISTS),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

GET_RESPONSE_DESCRIPTION = """

- Exemplo de resposta:

        {
            "cpf": "123.456.789-00",
            "name": "John Doe",
            "phone": "(00) 90000-0000",
            "phone_optional": "(00) 9000-0001",
            "email": "john@example",
            "level": '1'
        }
        

"""
GET_DESCRIPTION="""
Busca um usuário ao banco de dados.
             
- Exemplo de requisição:
             
        
        "user_id": "123.456.789-00"
        
          
""" + GET_RESPONSE_DESCRIPTION
GET_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, str(USER_RESPONSE_EXAMPLE)),
        generate_response(404, ERROR_NOT_ID),
        generate_response(404, ERROR_NOT_FOUND_USER),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

LIST_RESPONSE_DESCRIPTION = f""""""
LIST_DESCRIPTION="""""" + LIST_RESPONSE_DESCRIPTION
LIST_RESPONSES = None

UPDATE_RESPONSE_DESCRIPTION = f""""""
UPDATE_DESCRIPTION="""""" + UPDATE_RESPONSE_DESCRIPTION
UPDATE_RESPONSES = None

DELETE_RESPONSE_DESCRIPTION = f""""""
DELETE_DESCRIPTION="""""" + DELETE_RESPONSE_DESCRIPTION
DELETE_RESPONSES = None

LOGIN_RESPONSE_DESCRIPTION = f""""""
LOGIN_DESCRIPTION="""""" + LOGIN_RESPONSE_DESCRIPTION
LOGIN_RESPONSES = None
