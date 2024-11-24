# from fastapi import HTTPException
# from pytest import raises


# from constants.base import ERROR_INVALID_CPF
# from constants.classes import(
#   ERROR_CLASSES_REQUIRED_FIELD_NAME,
#   ERROR_CLASSES_REQUIRED_FIELD_ROOM,
#   ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF  
# )
# from schemas.classes import (
#     ClassRequest,
#     ClassEventRequest,
#     ClassStudentRequest,
#     ClassResponse
# )
# from utils.format import unformat_cpf


# def test_ClassRequest_success():
#     data = {
#         "name": "Matemática",
#         "room": "Sala 01",
#         "teacher_cpf": "123.456.789-00"
#     }
#     schema = ClassRequest(**data)
#     assert schema.name == data["name"]
#     assert schema.room == data["room"]
#     assert schema.teacher_cpf == unformat_cpf(data["teacher_cpf"])


# def test_ClassRequest_fail_no_name():
#     data = {
#         "room": "Sala 01",
#         "teacher_cpf": "123.456.789-00"
#     }
#     with raises(HTTPException) as e:
#         ClassRequest(**data)
    
#     e.value.status_code == 400
#     e.value.detail == ERROR_CLASSES_REQUIRED_FIELD_NAME


# def test_ClassRequest_fail_no_room():
#     data = {
#         "name": "Matemática",
#         "teacher_cpf": "123.456.789-00"
#     }
#     with raises(HTTPException) as e:
#         ClassRequest(**data)
    
#     e.value.status_code == 400
#     e.value.detail == ERROR_CLASSES_REQUIRED_FIELD_ROOM


# def test_classRequest_fail_no_teacher_cpf():
#     data = {
#         "name": "Matemática",
#         "room": "Sala 01"
#     }
#     with raises(HTTPException) as e:
#         ClassRequest(**data)
    
#     e.value.status_code == 400
#     e.value.detail == ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF


# def test_ClassRequest_fail_invalid_teacher_cpf():
#     data = {
#         "name": "Matemática",
#         "room": "Sala 01",
#         "teacher_cpf": "123.456.789-011"
#     }
#     with raises(HTTPException) as e:
#         ClassRequest(**data)
    
#     e.value.status_code == 400
#     e.value.detail == ERROR_INVALID_CPF