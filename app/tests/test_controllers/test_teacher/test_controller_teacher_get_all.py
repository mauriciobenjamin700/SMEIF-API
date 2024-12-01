from fastapi import HTTPException
from pytest import raises


from constants.teacher import ERROR_TEACHER_GET_ALL_NOT_FOUND
from controllers.teacher import TeacherController
from schemas.base import UserLevel
from utils.format import format_cpf, format_phone


def test_controller_teacher_get_all_success(
    db_session,
    mock_teacher_on_db
):
    
    controller = TeacherController(db_session)

    response = controller.get_all()

    assert len(response) == 1

    response = response[0]

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf)
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone)
    assert response.user.level == UserLevel.TEACHER.value

    assert response.disciplines == []
    assert response.classes == []


def test_controller_teacher_get_all_with_no_teacher(db_session, mock_user_on_db):
    
    controller = TeacherController(db_session)

    with raises(HTTPException)  as e:

        controller.get_all()

    
    assert e.value.status_code == 404
    assert e.value.detail == ERROR_TEACHER_GET_ALL_NOT_FOUND