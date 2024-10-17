from fastapi import Response


from constants.base import ERROR_SERVER_ERROR
from constants.user import (
    ERROR_CPF_ALREADY_EXISTS, 
    ERROR_EMAIL_ALREADY_EXISTS, 
    ERROR_PHONE_ALREADY_EXISTS, 
    MESSAGE_ADD_SUCESS
)
from utils.messages import generate_response, generate_responses_documentation


ADD_DESCRIPTION = """
Add a new client in the database
             
- Example:
             
        {
            "cpf": "123.456.789-00",
            "name": "John Doe",
            "phone": "(00) 90000-0000",
            "phone_optional": "(00) 9000-0001",
            "email": " jhon.doe@example.com",
            "password": 123,
            "level": 1
        }
             
"""
ADD_RESPONSE_DESCRIPTION = f"""


            "detail": "{MESSAGE_ADD_SUCESS}"
        

"""

ADD_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_ADD_SUCESS),
        generate_response(409, ERROR_CPF_ALREADY_EXISTS),
        generate_response(409, ERROR_PHONE_ALREADY_EXISTS),
        generate_response(409, ERROR_EMAIL_ALREADY_EXISTS),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
    )