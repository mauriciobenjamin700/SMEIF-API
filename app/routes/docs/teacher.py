from constants.base import ERROR_SERVER_ERROR
from constants.classes import ERROR_CLASSES_GET_ALL_NOT_FOUND
from constants.disciplines import ERROR_DISCIPLINES_GET_ALL_NOT_FOUND
from constants.teacher import (
    ERROR_TEACHER_ADD_CLASSES_CONFLICT, 
    ERROR_TEACHER_ADD_DISCIPLINES_CONFLICT,
    ERROR_TEACHER_GET_ALL_NOT_FOUND
)
from constants.user import (
    ERROR_USER_GET_TEACHER_NOT_FOUND, 
    ERROR_USER_INVALID_TEACHER_LEVEL
)
from utils.messages.doc import (
    generate_response, 
    generate_responses_documentation
)


ADD_CLASS_DESCRIPTION = "Atribui uma lista de turmas ao um professor"
ADD_DISCIPLINES_DESCRIPTION = "Atribui uma lista de disciplinas ao um professor"
GET_TEACHER_DESCRIPTION = "Retorna dados de um professor específico"
LIST_TEACHER_DESCRIPTION = "Retorna uma lista de professores"
DELETE_CLASS_DESCRIPTION = "Remove uma lista de turmas de um professor"
DELETE_DISCIPLINES_DESCRIPTION = "Remove uma lista de disciplinas de um professor"

ADD_CLASS_RESPONSES = generate_responses_documentation(
    [
        generate_response(400, ERROR_USER_INVALID_TEACHER_LEVEL),
        generate_response(404, ERROR_USER_GET_TEACHER_NOT_FOUND),
        generate_response(409, ERROR_TEACHER_ADD_CLASSES_CONFLICT),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)
ADD_DISCIPLINES_RESPONSES = generate_responses_documentation(
    [
        generate_response(400, ERROR_USER_INVALID_TEACHER_LEVEL),
        generate_response(404, ERROR_USER_GET_TEACHER_NOT_FOUND),
        generate_response(409, ERROR_TEACHER_ADD_DISCIPLINES_CONFLICT),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)
GET_TEACHER_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_USER_GET_TEACHER_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)
LIST_TEACHER_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_TEACHER_GET_ALL_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)
DELETE_CLASS_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_USER_GET_TEACHER_NOT_FOUND),
        generate_response(404, ERROR_CLASSES_GET_ALL_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)
DELETE_DISCIPLINES_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_USER_GET_TEACHER_NOT_FOUND),
        generate_response(404, ERROR_DISCIPLINES_GET_ALL_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)