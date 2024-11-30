from constants.base import ERROR_SERVER_ERROR
from constants.disciplines import (
    ERROR_DISCIPLINES_ADD_CONFLICT,
    ERROR_DISCIPLINES_GET_ALL_NOT_FOUND,
    ERROR_DISCIPLINES_GET_NOT_FOUND,
    ERROR_DISCIPLINES_REQUIRED_FIELD_NAME, 
    MESSAGE_DISCIPLINE_ADD_SUCCESS,
    MESSAGE_DISCIPLINE_DELETE_SUCCESS
)
from utils.messages.doc import (
    generate_response, 
    generate_responses_documentation
)


ADD_DESCRIPTION = "Cadastra uma disciplina no banco de dados"
GET_DESCRIPTION = "Retorna uma disciplina do banco de dados"
LIST_DESCRIPTION = "Retorna todas as disciplinas do banco de dados"
UPDATE_DESCRIPTION = "Atualiza uma disciplina no banco de dados"
DELETE_DESCRIPTION = "Deleta uma disciplina do banco de dados"


ADD_RESPONSES = generate_responses_documentation(
    [
        generate_response(201, MESSAGE_DISCIPLINE_ADD_SUCCESS),
        generate_response(409, ERROR_DISCIPLINES_ADD_CONFLICT),
        generate_response(422, ERROR_DISCIPLINES_REQUIRED_FIELD_NAME),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

GET_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_DISCIPLINES_GET_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]

)

LIST_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_DISCIPLINES_GET_ALL_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

UPDATE_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_DISCIPLINES_GET_NOT_FOUND),
        generate_response(422, ERROR_DISCIPLINES_REQUIRED_FIELD_NAME),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

DELETE_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_DISCIPLINE_DELETE_SUCCESS),
        generate_response(404, ERROR_DISCIPLINES_GET_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)