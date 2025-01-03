from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import ERROR_CHILD_GET_ALL_NOT_FOUND
from useCases.student import StudentUseCases


def test_StudentUseCases_get_all_success(
    db_session: Session,
    mock_student_on_db
):
    # Arrange

    uc = StudentUseCases(db_session)

    # Act
    response = uc.get_all()

    # Assert
    assert isinstance(response, list)
    assert len(response) > 0
    assert response[0].name == mock_student_on_db.name
    assert isinstance(response[0].matriculation, str)
    assert isinstance(response[0].class_info, str)
    assert isinstance(response[0].shift, str)


def test_StudentUseCases_get_all_fail_empty(
    db_session: Session
):
    # Arrange

    uc = StudentUseCases(db_session)

    # Act
    with raises(HTTPException) as exception:
        uc.get_all()

    # Assert
    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CHILD_GET_ALL_NOT_FOUND