from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import ERROR_CHILD_GET_NOT_FOUND
from useCases.student import StudentUseCases
from utils.format import format_date


def test_StudentUseCases_update_success(
    db_session: Session,
    mock_student_on_db,
    mock_ChildRequest_update
):
    # Arrange
    student_uc = StudentUseCases(db_session)
    request = mock_ChildRequest_update

    # Act
    response = student_uc.update(
        request=request
    )

    db_session.refresh(mock_student_on_db)

    # Assert
    assert response.name == mock_student_on_db.name
    assert isinstance(response.matriculation, str)
    assert isinstance(response.class_info, str)
    assert isinstance(response.shift, str)
    assert request.birth_date == format_date(mock_student_on_db.birth_date, False)
    assert request.address.state == mock_student_on_db.state
    assert request.address.city == mock_student_on_db.city
    assert request.address.neighborhood == mock_student_on_db.neighborhood
    assert request.address.street == mock_student_on_db.street
    assert request.address.house_number == mock_student_on_db.house_number
    assert request.address.complement == mock_student_on_db.complement
    assert request.dependencies == mock_student_on_db.dependencies


def test_StudentUseCases_update_fail_empty(
    db_session: Session,
    mock_ChildRequest_update
):
    
    # Arrange
    uc = StudentUseCases(db_session)
    request = mock_ChildRequest_update
    request.cpf = "123.123.123-12"


    # Act


    with raises(HTTPException) as e:
        uc.update(
            request=request
        )

    
    # Assert

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_CHILD_GET_NOT_FOUND