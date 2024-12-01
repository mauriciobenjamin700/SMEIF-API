from fastapi import HTTPException
from pytest import raises


from constants.base import (
    ERROR_INVALID_CPF
)
from constants.teacher import (
    ERROR_TEACHER_INVALID_FIELD_CLASSES,
    ERROR_TEACHER_INVALID_FIELD_DISCIPLINES,
    ERROR_TEACHER_REQUIRED_FIELD_CLASSES,
    ERROR_TEACHER_REQUIRED_FIELD_DISCIPLINES
)
from schemas.teacher import (
    TeacherDisciplinesRequest,
    ClassTeacherRequest,
    TeacherResponse
)
from utils.format import unformat_cpf

def test_schema_TeacherDisciplinesRequest_success(mock_teacher_disciplines_request_data):

    schema = TeacherDisciplinesRequest(**mock_teacher_disciplines_request_data)

    assert schema.user_cpf == unformat_cpf(mock_teacher_disciplines_request_data["user_cpf"])
    assert schema.disciplines_id == mock_teacher_disciplines_request_data["disciplines_id"]


def test_schema_TeacherDisciplinesRequest_fail_invalid_cpf(mock_teacher_disciplines_request_data):

    data = mock_teacher_disciplines_request_data.copy()

    data["user_cpf"] = "123.456.789-0"

    with raises(HTTPException) as e:
        TeacherDisciplinesRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF


def test_schema_TeacherDisciplinesRequest_fail_invalid_disciplines_id(mock_teacher_disciplines_request_data):

    data = mock_teacher_disciplines_request_data.copy()

    data["disciplines_id"] = "123"

    with raises(HTTPException) as e:
        TeacherDisciplinesRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_TEACHER_INVALID_FIELD_DISCIPLINES


def test_schema_TeacherDisciplinesRequest_fail_invalid_disciplines_id_empty(mock_teacher_disciplines_request_data):

    data = mock_teacher_disciplines_request_data.copy()

    data["disciplines_id"] = []

    with raises(HTTPException) as e:
        TeacherDisciplinesRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_TEACHER_REQUIRED_FIELD_DISCIPLINES


def test_schema_TeacherDisciplinesRequest_fail_invalid_disciplines_id_element(mock_teacher_disciplines_request_data):
    
        data = mock_teacher_disciplines_request_data.copy()
    
        data["disciplines_id"] = [123]
    
        with raises(HTTPException) as e:
            TeacherDisciplinesRequest(**data)
    
        assert e.value.status_code == 422
        assert e.value.detail == ERROR_TEACHER_INVALID_FIELD_DISCIPLINES

def test_schemas_ClassTeacherRequest_success(mock_class_teacher_request_data):

    schema = ClassTeacherRequest(**mock_class_teacher_request_data)

    assert schema.user_cpf == unformat_cpf(mock_class_teacher_request_data["user_cpf"])
    assert schema.classes_id == mock_class_teacher_request_data["classes_id"]


def test_schemas_ClassTeacherRequest_fail_invalid_cpf(mock_class_teacher_request_data):

    data = mock_class_teacher_request_data.copy()

    data["user_cpf"] = "123.456.789-0"

    with raises(HTTPException) as e:
        ClassTeacherRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF


def test_schemas_ClassTeacherRequest_fail_invalid_classes_id(mock_class_teacher_request_data):

    data = mock_class_teacher_request_data.copy()

    data["classes_id"] = "123"

    with raises(HTTPException) as e:
        ClassTeacherRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_TEACHER_INVALID_FIELD_CLASSES

def test_schemas_ClassTeacherRequest_fail_invalid_classes_id_empty(mock_class_teacher_request_data):
    
        data = mock_class_teacher_request_data.copy()
    
        data["classes_id"] = []
    
        with raises(HTTPException) as e:
            ClassTeacherRequest(**data)
    
        assert e.value.status_code == 422
        assert e.value.detail == ERROR_TEACHER_REQUIRED_FIELD_CLASSES


def test_schemas_ClassTeacherRequest_fail_invalid_classes_id_element(mock_class_teacher_request_data):
    
        data = mock_class_teacher_request_data.copy()
    
        data["classes_id"] = [123]
    
        with raises(HTTPException) as e:
            ClassTeacherRequest(**data)
    
        assert e.value.status_code == 422
        assert e.value.detail == ERROR_TEACHER_INVALID_FIELD_CLASSES