from constants.base import ERROR_INVALID_CPF, ERROR_SERVER_ERROR
from constants.child import ERROR_CHILD_GET_NOT_FOUND
from constants.classes import ERROR_CLASSES_GET_NOT_FOUND
from constants.disciplines import ERROR_DISCIPLINES_GET_NOT_FOUND
from constants.note import (
    ERROR_NOTE_ALREADY_ADD,
    ERROR_NOTE_INVALID_FIELD_AVAL_NUMBER,
    ERROR_NOTE_INVALID_FIELD_POINTS,
    ERROR_NOTE_NOT_FOUND,
    ERROR_NOTE_NOT_FOUND_NOTES,
    ERROR_NOTE_REQUIRED_FIELD_AVAL_NUMBER,
    ERROR_NOTE_REQUIRED_FIELD_CHILD_CPF,
    ERROR_NOTE_REQUIRED_FIELD_CLASS_ID,
    ERROR_NOTE_REQUIRED_FIELD_DISCIPLINES_ID,
    ERROR_NOTE_REQUIRED_FIELD_POINTS,
    ERROR_NOTE_REQUIRED_FIELD_SEMESTER,
    SUCCESS_NOTE_ADD,
    SUCCESS_NOTE_DELETE
)
from utils.messages.doc import (
    generate_response, 
    generate_responses_documentation
)


ADD_DESCRIPTION = "Cadastra uma nova nota no banco de dados"
LIST_DESCRIPTION = "Retorna todas as notas do banco de dados, podendo filtrar por critérios via query params"
UPDATE_DESCRIPTION = "Atualiza uma nota no banco de dados"
DELETE_DESCRIPTION = "Deleta uma nota do banco de dados"


ADD_RESPONSES = generate_responses_documentation(
    [
        generate_response(201, SUCCESS_NOTE_ADD),
        generate_response(404, ERROR_DISCIPLINES_GET_NOT_FOUND),
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),
        generate_response(404, ERROR_CHILD_GET_NOT_FOUND),
        generate_response(409, ERROR_NOTE_ALREADY_ADD),
        generate_response(422, ERROR_NOTE_REQUIRED_FIELD_SEMESTER),
        generate_response(422, ERROR_NOTE_INVALID_FIELD_POINTS),
        generate_response(422, ERROR_NOTE_REQUIRED_FIELD_AVAL_NUMBER),
        generate_response(422, ERROR_NOTE_INVALID_FIELD_AVAL_NUMBER),
        generate_response(422, ERROR_NOTE_REQUIRED_FIELD_POINTS),
        generate_response(422, ERROR_NOTE_REQUIRED_FIELD_DISCIPLINES_ID),
        generate_response(422, ERROR_NOTE_REQUIRED_FIELD_CLASS_ID),
        generate_response(422, ERROR_NOTE_REQUIRED_FIELD_CHILD_CPF),
        generate_response(422, ERROR_INVALID_CPF),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

LIST_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_NOTE_NOT_FOUND_NOTES),
        generate_response(422, ERROR_INVALID_CPF),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)


UPDATE_RESPONSES = generate_responses_documentation(
    [
        generate_response(422, ERROR_NOTE_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

DELETE_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, SUCCESS_NOTE_DELETE),
        generate_response(422, ERROR_NOTE_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)