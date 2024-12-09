from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import (
    ERROR_CHILD_ADD_CONFLICT_FIELD_CPF,
    ERROR_CHILD_ADD_NOT_FOUND_PARENT
)
from controllers.student import StudentController
from database.models import (
    ChildModel,
    ClassStudentModel,
    ChildParentsModel,
)
from schemas.child import StudentResponse


def test_StudentController_add_success(
    db_session: Session,
    mock_StudentRequest
):
    # Arrange
    controller = StudentController(db_session)
    request = mock_StudentRequest

    # Act
    response = controller.add(request)

    child = db_session.query(ChildModel).filter_by(cpf=request.cpf).first()

    class_student = db_session.query(ClassStudentModel).filter_by(child_cpf=request.cpf).first()

    child_parents = db_session.query(ChildParentsModel).filter_by(child_cpf=request.cpf).first()

    # Assert
    assert isinstance(response, StudentResponse)
    assert isinstance(response.matriculation, str)
    assert response.name == request.name
    assert isinstance(response.class_info, str)
    assert isinstance(response.shift, str)
    assert child is not None
    assert class_student is not None
    assert child_parents is not None


def test_StudentController_add_fail_already_exists(
    db_session,
    mock_StudentRequest,
    mock_student_on_db
):
    # Arrange
    controller = StudentController(db_session)
    request = mock_StudentRequest

    # Act
    with raises(HTTPException) as exception:
        controller.add(request)

    # Assert
    assert exception.value.status_code == 409
    assert exception.value.detail == ERROR_CHILD_ADD_CONFLICT_FIELD_CPF


def test_StudentController_add_fail_parent_not_found(
    db_session,
    mock_StudentRequest,
):
    # Arrange
    controller = StudentController(db_session)
    request = mock_StudentRequest
    request.parent_cpf = "123.456.789-00"

    # Act
    with raises(HTTPException) as exception:
        controller.add(request)

    # Assert
    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CHILD_ADD_NOT_FOUND_PARENT