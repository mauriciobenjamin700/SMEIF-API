from constants.address import (
    ERROR_ADDRESS_REQUIRED_FIELD_HOUSE_NUMBER,
    ERROR_ADDRESS_REQUIRED_FIELD_NEIGHBORHOOD,
    ERROR_ADDRESS_REQUIRED_FIELD_STATE,
    ERROR_ADDRESS_REQUIRED_FIELD_STREET,
    ERROR_ADDRESS_REQUIRED_FIELD_CITY
)
from constants.base import (
    ERROR_INVALID_CPF, 
    ERROR_INVALID_EMAIL, 
    ERROR_INVALID_FORMAT_BIRTH_DATE, 
    ERROR_INVALID_FORMAT_GENDER, 
    ERROR_INVALID_PHONE, 
    ERROR_INVALID_PHONE_OPTIONAL, 
    ERROR_SERVER_ERROR
)
from constants.user import (
    ERROR_USER_CPF_ALREADY_EXISTS, 
    ERROR_USER_EMAIL_ALREADY_EXISTS,
    ERROR_USER_INVALID_BIRTHDATE,
    ERROR_USER_INVALID_LEVEL,
    ERROR_USER_NOT_FOUND_USER,
    ERROR_USER_NOT_FOUND_USERS,
    ERROR_USER_PASSWORD_WRONG, 
    ERROR_USER_PHONE_ALREADY_EXISTS,
    ERROR_USER_PHONE_AND_OPTIONAL_PHONE_EQUALS,
    ERROR_USER_REQUIRED_FIELD_ADDRESS,
    ERROR_USER_REQUIRED_FIELD_BIRTH_DATE,
    ERROR_USER_REQUIRED_FIELD_CPF,
    ERROR_USER_REQUIRED_FIELD_EMAIL,
    ERROR_USER_REQUIRED_FIELD_GENDER,
    ERROR_USER_REQUIRED_FIELD_NAME,
    ERROR_USER_REQUIRED_FIELD_PASSWORD,
    ERROR_USER_REQUIRED_FIELD_PHONE, 
    MESSAGE_USER_ADD_SUCCESS,
    MESSAGE_USER_DELETE_SUCCESS,
    MESSAGE_USER_UPDATE_FAIL,
    MESSAGE_USER_UPDATE_SUCCESS
)
from utils.messages.doc import (
    generate_response, 
    generate_responses_documentation
)


ADD_DESCRIPTION = "Realiza o cadastro de um usuário no banco de dados com os dados fornecidos"
ADD_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_USER_ADD_SUCCESS),
        generate_response(409, ERROR_USER_CPF_ALREADY_EXISTS),
        generate_response(409, ERROR_USER_PHONE_ALREADY_EXISTS),
        generate_response(409, ERROR_USER_EMAIL_ALREADY_EXISTS),
        generate_response(422, ERROR_USER_REQUIRED_FIELD_CPF),
        generate_response(422, ERROR_INVALID_CPF),
        generate_response(422, ERROR_USER_REQUIRED_FIELD_NAME),
        generate_response(422, ERROR_USER_REQUIRED_FIELD_BIRTH_DATE),
        generate_response(422, ERROR_INVALID_FORMAT_BIRTH_DATE),
        generate_response(422, ERROR_USER_INVALID_BIRTHDATE),
        generate_response(422, ERROR_USER_REQUIRED_FIELD_GENDER),
        generate_response(422, ERROR_INVALID_FORMAT_GENDER),
        generate_response(422, ERROR_USER_REQUIRED_FIELD_PHONE),
        generate_response(422, ERROR_INVALID_PHONE),
        generate_response(422, ERROR_INVALID_PHONE_OPTIONAL),
        generate_response(422, ERROR_USER_PHONE_AND_OPTIONAL_PHONE_EQUALS),
        generate_response(422, ERROR_USER_REQUIRED_FIELD_EMAIL),
        generate_response(422, ERROR_INVALID_EMAIL),
        generate_response(422, ERROR_USER_REQUIRED_FIELD_PASSWORD),
        generate_response(422, ERROR_USER_INVALID_LEVEL),
        generate_response(422, ERROR_USER_REQUIRED_FIELD_ADDRESS),
        generate_response(422, ERROR_ADDRESS_REQUIRED_FIELD_STATE),
        generate_response(422, ERROR_ADDRESS_REQUIRED_FIELD_CITY),
        generate_response(422, ERROR_ADDRESS_REQUIRED_FIELD_NEIGHBORHOOD),
        generate_response(422, ERROR_ADDRESS_REQUIRED_FIELD_STREET),
        generate_response(422, ERROR_ADDRESS_REQUIRED_FIELD_HOUSE_NUMBER),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)


GET_DESCRIPTION="Busca um usuário no banco de dados."

GET_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_USER_REQUIRED_FIELD_CPF),
        generate_response(404, ERROR_USER_NOT_FOUND_USER),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)


LIST_DESCRIPTION="Busca todos os usuários no banco de dados."
LIST_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_USER_NOT_FOUND_USERS),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)


UPDATE_DESCRIPTION="Atualiza os dados de um usuário no banco de dados."
UPDATE_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_USER_UPDATE_SUCCESS),
        generate_response(200, MESSAGE_USER_UPDATE_FAIL),
        generate_response(404, ERROR_USER_REQUIRED_FIELD_CPF),
        generate_response(404, ERROR_USER_NOT_FOUND_USER),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)


DELETE_DESCRIPTION="Deleta um usuário do banco de dados."
DELETE_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_USER_DELETE_SUCCESS),
        generate_response(404, ERROR_USER_REQUIRED_FIELD_CPF),
        generate_response(404, ERROR_USER_NOT_FOUND_USER),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)


LOGIN_DESCRIPTION="Realiza o login de um usuário e retorna um token de autenticação."
LOGIN_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_USER_NOT_FOUND_USER),
        generate_response(401, ERROR_USER_PASSWORD_WRONG),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

