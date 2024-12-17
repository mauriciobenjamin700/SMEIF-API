from constants.base import (
    ERROR_INVALID_CPF,
    ERROR_INVALID_FORMAT_BIRTH_DATE,
    ERROR_INVALID_FORMAT_GENDER,
    ERROR_INVALID_FORMAT_SHIFT
)
from constants.classes import ERROR_CLASSES_GET_NOT_FOUND
from constants.child import (
    ERROR_CHILD_ADD_CONFLICT_FIELD_CPF,
    ERROR_CHILD_ADD_NOT_FOUND_PARENT,
    ERROR_CHILD_ADD_PARENT_ALREADY_ASSOCIATE_PARENT,
    ERROR_CHILD_ADD_PARENT_LIMIT_REACHED,
    ERROR_CHILD_CHANGE_CLASS_STUDENT_ALREADY_ASSOCIATE,
    ERROR_CHILD_DELETE_PARENT_LIMIT_REACHED,
    ERROR_CHILD_DELETE_PARENT_NOT_ASSOCIATE_PARENT,
    ERROR_CHILD_GET_ALL_NOT_FOUND,
    ERROR_CHILD_GET_CLASS_STUDENT_NOT_FOUND,
    ERROR_CHILD_GET_NOT_FOUND,
    ERROR_CHILD_INVALID_FIELD_BIRTH_DATE,
    ERROR_CHILD_INVALID_FIELD_KINSHIP,
    ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE,
    ERROR_CHILD_REQUIRED_FIELD_CLASS_ID,
    ERROR_CHILD_REQUIRED_FIELD_CPF,
    ERROR_CHILD_REQUIRED_FIELD_GENDER,
    ERROR_CHILD_REQUIRED_FIELD_KINSHIP,
    ERROR_CHILD_REQUIRED_FIELD_NAME,
    ERROR_CHILD_REQUIRED_FIELD_PARENT_CPF,
)
from utils.messages.doc import(
    generate_response,
    generate_responses_documentation
)


ADD_DESCRIPTION = "Cadastra um estudante no sistema"
GET_DESCRIPTION = "Retorna um estudante do sistema pelo CPF"
LIST_DESCRIPTION = "Retorna todos os estudantes do sistema"
UPDATE_DESCRIPTION = "Atualiza um estudante no sistema com base em seu CPF"
DELETE_DESCRIPTION = "Deleta um estudante do sistema com base em seu CPF"
CHANGE_CLASS_DESCRIPTION = "Troca um estudante do sistema de turma"
ADD_PARENT_DESCRIPTION = "Associa um estudante do sistema a um usuário responsável por ele"
REMOVE_PARENT_DESCRIPTION = "Desassocia um estudante do sistema de um usuário responsável por ele"


ADD_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CHILD_ADD_NOT_FOUND_PARENT),
        generate_response(409, ERROR_CHILD_ADD_CONFLICT_FIELD_CPF),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_CPF),
        generate_response(422, ERROR_INVALID_CPF),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_NAME),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE),
        generate_response(422, ERROR_INVALID_FORMAT_BIRTH_DATE),
        generate_response(422, ERROR_CHILD_INVALID_FIELD_BIRTH_DATE),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_GENDER),
        generate_response(422, ERROR_INVALID_FORMAT_GENDER),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_CLASS_ID),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_KINSHIP),
        generate_response(422, ERROR_CHILD_INVALID_FIELD_KINSHIP),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_PARENT_CPF),
        generate_response(422, ERROR_INVALID_FORMAT_SHIFT),
    ]
)

GET_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CHILD_GET_NOT_FOUND),
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),
        generate_response(422, ERROR_INVALID_CPF),
    ]
)

LIST_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CHILD_GET_ALL_NOT_FOUND),
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),

    ]
)

UPDATE_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CHILD_GET_NOT_FOUND),
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_CPF),
        generate_response(422, ERROR_INVALID_CPF),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_NAME),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE),
        generate_response(422, ERROR_INVALID_FORMAT_BIRTH_DATE),
        generate_response(422, ERROR_CHILD_INVALID_FIELD_BIRTH_DATE),
        generate_response(422, ERROR_CHILD_INVALID_FIELD_BIRTH_DATE),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_GENDER),
        generate_response(422, ERROR_INVALID_FORMAT_GENDER)

    ]
)

DELETE_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CHILD_GET_NOT_FOUND),
    ]
)

CHANGE_CLASS_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CHILD_GET_NOT_FOUND),
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),
        generate_response(404, ERROR_CHILD_GET_CLASS_STUDENT_NOT_FOUND),
        generate_response(404, ERROR_CLASSES_GET_NOT_FOUND),
        generate_response(422, ERROR_INVALID_CPF),
        generate_response(422, ERROR_CHILD_REQUIRED_FIELD_CLASS_ID),
        generate_response(409, ERROR_CHILD_CHANGE_CLASS_STUDENT_ALREADY_ASSOCIATE)
        
    ]
)

ADD_PARENT_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CHILD_ADD_NOT_FOUND_PARENT),
        generate_response(404, ERROR_CHILD_GET_NOT_FOUND),
        generate_response(409, ERROR_CHILD_ADD_PARENT_ALREADY_ASSOCIATE_PARENT),
        generate_response(409, ERROR_CHILD_ADD_PARENT_LIMIT_REACHED),
        generate_response(422, ERROR_CHILD_INVALID_FIELD_KINSHIP),
        generate_response(422, ERROR_INVALID_FORMAT_SHIFT),
    ]
)

REMOVE_PARENT_RESPONSES = generate_responses_documentation(
    [
        generate_response(404, ERROR_CHILD_ADD_NOT_FOUND_PARENT),
        generate_response(404, ERROR_CHILD_GET_NOT_FOUND),
        generate_response(404, ERROR_CHILD_DELETE_PARENT_NOT_ASSOCIATE_PARENT),
        generate_response(409, ERROR_CHILD_DELETE_PARENT_LIMIT_REACHED),
    ]
)