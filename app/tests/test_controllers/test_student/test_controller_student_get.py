from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import ERROR_CHILD_GET_NOT_FOUND
from controllers.student import StudentController


def test_StudentController_get_success(
    db_session: Session,
    mock_student_on_db
):
    # Arrange
    cpf = mock_student_on_db.cpf
    controller = StudentController(db_session)

    # Act
    response = controller.get(cpf)

    # Assert
    assert response.name == mock_student_on_db.name
    assert isinstance(response.matriculation, str)
    assert isinstance(response.class_info, str)
    assert isinstance(response.shift, str)


def test_StudentController_get_fail_empty(
    db_session: Session
):
    # Arrange

    controller = StudentController(db_session)

    # Act
    with raises(HTTPException) as exception:
        controller.get("123")

    # Assert
    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CHILD_GET_NOT_FOUND