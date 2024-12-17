from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import(
    ERROR_CHILD_GET_NOT_FOUND,
    MESSAGE_CHILD_DELETE_SUCCESS
)
from controllers.student import StudentController
from database.models import (
    ChildModel,
    ClassStudentModel,
    ChildParentsModel
)
from utils.format import format_cpf


def test_StudentController_delete_success(
    db_session: Session,
    mock_student_on_db,
):

    # Arrange

    cpf = format_cpf(mock_student_on_db.cpf)

    controller = StudentController(db_session)

    # Act
    response = controller.delete(cpf)

    child = db_session.query(ChildModel).filter_by(cpf=cpf).first()

    class_student = db_session.query(ClassStudentModel).filter_by(child_cpf=cpf).first()

    child_parents = db_session.query(ChildParentsModel).filter_by(child_cpf=cpf).first()

    # Assert
    assert response.detail == MESSAGE_CHILD_DELETE_SUCCESS
    assert child is None
    assert class_student is None
    assert child_parents is None


def test_StudentController_delete_success_unformat_cpf(
    db_session: Session,
    mock_student_on_db,
):

    # Arrange

    cpf = mock_student_on_db.cpf

    controller = StudentController(db_session)

    # Act
    response = controller.delete(cpf)

    child = db_session.query(ChildModel).filter_by(cpf=cpf).first()

    class_student = db_session.query(ClassStudentModel).filter_by(child_cpf=cpf).first()

    child_parents = db_session.query(ChildParentsModel).filter_by(child_cpf=cpf).first()

    # Assert
    assert response.detail == MESSAGE_CHILD_DELETE_SUCCESS
    assert child is None
    assert class_student is None
    assert child_parents is None


def test_StudentController_delete_fail_not_found(
    db_session: Session,
    mock_student_on_db,
):

    # Arrange

    cpf = "12345678900"

    controller = StudentController(db_session)

    # Act
    with raises(HTTPException) as exception:
        controller.delete(cpf)

    # Assert
    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CHILD_GET_NOT_FOUND