from fastapi import HTTPException
from pytest import raises


from constants.user import ERROR_USER_GET_TEACHER_NOT_FOUND
from useCases.teacher import TeacherUseCases
from schemas.base import UserLevel
from schemas.disciplines import DisciplineResponse
from schemas.classes import ClassResponse
from utils.format import (
    format_cpf, 
    format_phone
)


def test_uc_teacher_get_success_no_disciplines_and_no_classes(db_session, mock_teacher_on_db):
    uc = TeacherUseCases(db_session)

    response = uc.get(mock_teacher_on_db.cpf)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf)
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone)
    assert response.user.level == UserLevel.TEACHER.value

    assert response.disciplines == []
    assert response.classes == []


def test_uc_teacher_get_success_with_disciplines_and_classes(
    db_session, 
    mock_teacher_on_db, 
    mock_teacher_discipline_on_db, 
    mock_class_teacher_on_db
):

    uc = TeacherUseCases(db_session)

    response = uc.get(mock_teacher_on_db.cpf)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf)
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone)
    assert response.user.level == UserLevel.TEACHER.value

    assert isinstance(response.disciplines[0], DisciplineResponse)
    assert response.disciplines[0].id == mock_teacher_discipline_on_db.discipline_id
    assert isinstance(response.classes[0], ClassResponse)
    assert response.classes[0].id == mock_class_teacher_on_db.class_id


def test_uc_teacher_get_with_classes_and_not_disciplines(
db_session, 
mock_teacher_on_db,
mock_class_teacher_on_db
):

    uc = TeacherUseCases(db_session)

    response = uc.get(mock_teacher_on_db.cpf)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf)
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone)
    assert response.user.level == UserLevel.TEACHER.value

    assert response.disciplines == []
    assert isinstance(response.classes[0], ClassResponse)
    assert response.classes[0].id == mock_class_teacher_on_db.class_id


def test_uc_teacher_get_with_disciplines_and_not_classes(
    db_session, 
    mock_teacher_on_db,
    mock_teacher_discipline_on_db
):

    uc = TeacherUseCases(db_session)

    response = uc.get(mock_teacher_on_db.cpf)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf)
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone)
    assert response.user.level == UserLevel.TEACHER.value

    assert isinstance(response.disciplines[0], DisciplineResponse)
    assert response.disciplines[0].id == mock_teacher_discipline_on_db.discipline_id
    assert response.classes == []


def test_uc_teacher_get_invalid_teacher(db_session, mock_user_on_db):
    uc = TeacherUseCases(db_session)

    with raises(HTTPException) as exception:

        uc.get(mock_user_on_db.cpf)

    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_USER_GET_TEACHER_NOT_FOUND