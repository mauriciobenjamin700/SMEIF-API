from fastapi import Response


from constants.base import ERROR_SERVER_ERROR
from constants.user import (
    ERROR_CPF_ALREADY_EXISTS, 
    ERROR_EMAIL_ALREADY_EXISTS,
    ERROR_USER_NOT_FOUND_USER,
    ERROR_USER_NOT_FOUND_USERS,
    ERROR_USER_NOT_ID,
    ERROR_USER_PASSWORD_WRONG, 
    ERROR_PHONE_ALREADY_EXISTS, 
    MESSAGE_ADD_SUCCESS,
    MESSAGE_DELETE_SUCCESS,
    MESSAGE_UPDATE_SUCCESS
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

from app.utils.messages.messages import generate_response, generate_responses_documentation


ADD_RESPONSE_DESCRIPTION = f"""

- Exemplo de resposta:

            "detail": "{MESSAGE_ADD_SUCCESS}"
        

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
        generate_response(200, MESSAGE_ADD_SUCCESS),
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
Busca um usuário no banco de dados.
             
- Exemplo de requisição:
             
        
        "user_id": "123.456.789-00"
        
          
""" + GET_RESPONSE_DESCRIPTION

GET_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, str(USER_RESPONSE_EXAMPLE)),
        generate_response(404, ERROR_USER_NOT_ID),
        generate_response(404, ERROR_USER_NOT_FOUND_USER),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

LIST_RESPONSE_DESCRIPTION = """
Busca todos os usuários no banco de dados.

- Exemplo de resposta:

        [
            {
                "cpf": "123.456.789-00",
                "name": "John Doe",
                "phone": "(00) 90000-0000",
                "phone_optional": "(00) 9000-0001",
                "email": "john@example",
                "level": '1'
            },

            {
                "cpf": "123.456.789-01",
                "name": "John Do",
                "phone": "(00) 92000-0000",
                "phone_optional": "(00) 9020-0001",
                "email": "john@example3",
                "level": '2'
            }
        ]
"""

LIST_DESCRIPTION="""""" + LIST_RESPONSE_DESCRIPTION
LIST_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, str([USER_RESPONSE_EXAMPLE, USER_RESPONSE_EXAMPLE])),
        generate_response(404, ERROR_USER_NOT_FOUND_USERS),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)


UPDATE_RESPONSE_DESCRIPTION = f"""

- Exemplo de resposta:

        "detail": "{MESSAGE_UPDATE_SUCCESS}"


"""

UPDATE_DESCRIPTION="""

- Exemplo de requisição:

        "cpf": "123.456.789-00",

        {
            "name": "John Doe2",
            "phone": "(00) 90000-6000",
            "phone_optional": "(00) 9002-0001",
        }

""" + UPDATE_RESPONSE_DESCRIPTION

UPDATE_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_UPDATE_SUCCESS),
        generate_response(404, ERROR_USER_NOT_ID),
        generate_response(404, ERROR_USER_NOT_FOUND_USER),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

DELETE_RESPONSE_DESCRIPTION = f"""
- Exemplo de resposta:
    
            "detail": "{MESSAGE_DELETE_SUCCESS}"

"""
DELETE_DESCRIPTION="""

Deleta um usuário no banco de dados.

- Exemplo de requisição:

        "user_id": "123.456.789-00"

""" + DELETE_RESPONSE_DESCRIPTION
DELETE_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_DELETE_SUCCESS),
        generate_response(404, ERROR_USER_NOT_ID),
        generate_response(404, ERROR_USER_NOT_FOUND_USER),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

LOGIN_RESPONSE_DESCRIPTION = """

- Exemplo de resposta:

        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

"""
LOGIN_DESCRIPTION="""

Realiza o login de um usuário e retorna um token de autenticação.

- Exemplo de requisição:

        {
            "cpf": "123.456.789-00",
            "password": "123"
        }

""" + LOGIN_RESPONSE_DESCRIPTION
LOGIN_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"),
        generate_response(404, ERROR_USER_NOT_FOUND_USER),
        generate_response(401, ERROR_USER_PASSWORD_WRONG),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)
