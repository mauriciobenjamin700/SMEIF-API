from constants.base import ERROR_SERVER_ERROR
from constants.classes import (
    ERROR_CLASS_ADD_CONFLICT,
    ERROR_CLASSES_EVENTS_ADD_CONFLICT,
    ERROR_CLASSES_EVENTS_ADD_RECURRENCES_CONFLICT,
    ERROR_CLASSES_EVENTS_DELETE_RECURRENCES_NOT_FOUND,
    ERROR_CLASSES_EVENTS_GET_ALL_NOT_FOUND,
    ERROR_CLASSES_EVENTS_GET_NOT_FOUND,
    ERROR_CLASSES_GET_ALL_NOT_FOUND,
    ERROR_CLASSES_GET_NOT_FOUND,
    ERROR_CLASSES_INVALID_FIELD_DAY_OF_WEEK,
    ERROR_CLASSES_INVALID_FIELD_EDUCATION_LEVEL,
    ERROR_CLASSES_INVALID_FIELD_END_DATE,
    ERROR_CLASSES_INVALID_FIELD_ID,
    ERROR_CLASSES_INVALID_FIELD_MAX_STUDENTS,
    ERROR_CLASSES_INVALID_FIELD_SHIFT,
    ERROR_CLASSES_INVALID_FIELD_START_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID,
    ERROR_CLASSES_REQUIRED_FIELD_DAY_OF_WEEK,
    ERROR_CLASSES_REQUIRED_FIELD_DISCIPLINES_ID, 
    ERROR_CLASSES_REQUIRED_FIELD_EDUCATION_LEVEL,
    ERROR_CLASSES_REQUIRED_FIELD_END_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_ID,
    ERROR_CLASSES_REQUIRED_FIELD_MAX_STUDENTS,
    ERROR_CLASSES_REQUIRED_FIELD_NAME,
    ERROR_CLASSES_REQUIRED_FIELD_RECURRENCES,
    ERROR_CLASSES_REQUIRED_FIELD_SHIFT,
    ERROR_CLASSES_REQUIRED_FIELD_START_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF, 
    MESSAGE_CLASS_ADD_SUCCESS,
    MESSAGE_CLASS_EVENT_ADD_SUCCESS,
    MESSAGE_CLASS_EVENT_DELETE_SUCCESS,
    MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS,
    MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS
)
from constants.disciplines import ERROR_DISCIPLINES_GET_NOT_FOUND
from constants.teacher import ERROR_TEACHER_GET_NOT_FOUND
from utils.messages.doc import (
    generate_response, 
    generate_responses_documentation
)


ADD_DESCRIPTION = "Cadastra uma turma no banco de dados"
GET_DESCRIPTION = "Retorna uma turma do banco de dados"
LIST_DESCRIPTION = "Retorna todas as turmas do banco de dados"
UPDATE_DESCRIPTION = "Atualiza uma turma no banco de dados"
DELETE_DESCRIPTION = "Deleta uma turma do banco de dados"
ADD_EVENT_DESCRIPTION = "Cadastra uma aula em uma turma"
GET_EVENT_DESCRIPTION = "Retorna uma aula com base em seu ID"
LIST_EVENTS_DESCRIPTION = "Retorna todas as aulas do banco de dados"
UPDATE_EVENT_DESCRIPTION = "Atualiza uma aula no banco de dados"
DELETE_EVENT_DESCRIPTION = "Deleta uma aula do banco de dados"
ADD_RECURRENCES_DESCRIPTION = "Adiciona recorrências a uma aula\n\nAs recorrências são adicionadas a partir da data de início da aula e se repetem de acordo com o intervalo e a quantidade de recorrências"
DELETE_RECURRENCES_DESCRIPTION = "Deleta as recorrências de uma aula"


ADD_RESPONSES = generate_responses_documentation(
    [
        generate_response(201, MESSAGE_CLASS_ADD_SUCCESS),
        generate_response(409, ERROR_CLASS_ADD_CONFLICT),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_EDUCATION_LEVEL),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_EDUCATION_LEVEL),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_NAME),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_ID),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_ID),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_SHIFT),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_SHIFT),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_MAX_STUDENTS),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_MAX_STUDENTS),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

GET_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]

)

LIST_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CLASSES_GET_ALL_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

UPDATE_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

DELETE_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_CLASS_ADD_SUCCESS),
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND)
    ]
)

ADD_EVENT_RESPONSES = generate_responses_documentation(
    [
        generate_response(201, MESSAGE_CLASS_EVENT_ADD_SUCCESS),
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),
        generate_response(404, ERROR_DISCIPLINES_GET_NOT_FOUND),
        generate_response(404, ERROR_TEACHER_GET_NOT_FOUND),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_DISCIPLINES_ID),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_START_DATE),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_START_DATE),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_END_DATE),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_END_DATE),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_RECURRENCES),
        generate_response(409, ERROR_CLASSES_EVENTS_ADD_CONFLICT),
        
    ]
)

GET_EVENT_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CLASSES_EVENTS_GET_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

LIST_EVENTS_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CLASSES_EVENTS_GET_ALL_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

UPDATE_EVENT_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CLASSES_EVENTS_GET_NOT_FOUND),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

DELETE_EVENT_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_CLASS_EVENT_DELETE_SUCCESS),
        generate_response(404, ERROR_CLASSES_EVENTS_GET_NOT_FOUND),
    ]
)

ADD_RECURRENCES_RESPONSES = generate_responses_documentation(
    [
        generate_response(201, MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS),
        generate_response(404, ERROR_CLASSES_EVENTS_GET_NOT_FOUND),
        generate_response(409, ERROR_CLASSES_EVENTS_ADD_RECURRENCES_CONFLICT),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_DAY_OF_WEEK),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_DAY_OF_WEEK),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_START_DATE),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_START_DATE),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_END_DATE),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_END_DATE),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)

DELETE_RECURRENCES_RESPONSES = generate_responses_documentation(
    [
        generate_response(200, MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS),
        generate_response(404, ERROR_CLASSES_EVENTS_GET_NOT_FOUND),
        generate_response(404, ERROR_CLASSES_EVENTS_DELETE_RECURRENCES_NOT_FOUND),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_DAY_OF_WEEK),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_DAY_OF_WEEK),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_START_DATE),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_START_DATE),
        generate_response(422, ERROR_CLASSES_REQUIRED_FIELD_END_DATE),
        generate_response(422, ERROR_CLASSES_INVALID_FIELD_END_DATE),
        generate_response(500, ERROR_SERVER_ERROR)
    ]
)