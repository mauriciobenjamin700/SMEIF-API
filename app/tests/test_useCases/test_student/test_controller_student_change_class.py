from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.base import ERROR_INVALID_CPF
from constants.classes import ERROR_CLASSES_GET_NOT_FOUND
from constants.child import (
    ERROR_CHILD_CHANGE_CLASS_STUDENT_ALREADY_ASSOCIATE,
    ERROR_CHILD_GET_NOT_FOUND,
    ERROR_CHILD_REQUIRED_FIELD_CLASS_ID
)
from useCases.student import StudentUseCases
from schemas.child import StudentResponse


def test_StudentUseCases_change_class_success_transfer(
    db_session: Session,
    mock_student_on_db,
    mock_new_class_on_db
):
    
    # Arrange
    uc = StudentUseCases(db_session)
    student_cpf = mock_student_on_db.cpf
    to_class_id = mock_new_class_on_db.id
    is_transfer = True
    
    
    # Act
    
    response = uc.change_class(
        student_cpf=student_cpf,
        to_class_id=to_class_id,
        is_transfer=is_transfer,
    )
    
    # Assert
    
    assert isinstance(response, StudentResponse)
    assert response.name == mock_student_on_db.name
    assert response.matriculation == mock_student_on_db.matriculation
    assert response.class_info == f"{mock_new_class_on_db.name} {mock_new_class_on_db.section}"
    assert response.shift == mock_new_class_on_db.shift
    
    
def test_StudentUseCases_change_class_success_aloc(
    db_session: Session,
    mock_student_on_db,
    mock_class_on_db
):
    
    # Arrange
    uc = StudentUseCases(db_session)
    student_cpf = mock_student_on_db.cpf
    to_class_id = mock_class_on_db.id
    is_transfer = False
    
    
    # Act
    
    response = uc.change_class(
        student_cpf=student_cpf,
        to_class_id=to_class_id,
        is_transfer=is_transfer,
    )
    
    # Assert
    
    assert isinstance(response, StudentResponse)
    assert response.name == mock_student_on_db.name
    assert response.matriculation == mock_student_on_db.matriculation
    assert response.class_info == f"{mock_class_on_db.name} {mock_class_on_db.section}"
    assert response.shift == mock_class_on_db.shift
    
    
def test_StudentUseCases_change_class_fail_invalid_cpf(
    db_session: Session,
    mock_student_on_db,
    mock_new_class_on_db
):
    
    # Arrange
    
    uc = StudentUseCases(db_session)
    student_cpf = "123.123.123-1"
    class_id = mock_new_class_on_db.id
    
    
    # Act
    
    with raises(HTTPException) as e:
        
        uc.change_class(
            student_cpf=student_cpf,
            to_class_id=class_id,
            is_transfer=True,
        )
        
    
    # Assert
    
    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF
    
    
def test_StudentUseCases_change_class_fail_empty_to_class_id(
    db_session: Session,
    mock_student_on_db,
):
    
    # Arrange
    
    uc = StudentUseCases(db_session)
    student_cpf = mock_student_on_db.cpf
    to_class_id = ""
    
    
    # Act
    
    with raises(HTTPException) as e:
        
        uc.change_class(
            student_cpf=student_cpf,
            to_class_id=to_class_id,
            is_transfer=True,
        )
        
    # Assert
    
    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_CLASS_ID
    
    
def test_StudentUseCases_change_class_fail_not_found_child(
    db_session: Session,
    mock_student_on_db,
    mock_new_class_on_db
):
    
    # Arrange
    
    uc = StudentUseCases(db_session)
    student_cpf = "123.456.789-22"
    to_class_id = mock_new_class_on_db.id
    
    
    # Act
    
    with raises(HTTPException) as e:
        
        uc.change_class(
            student_cpf=student_cpf,
            to_class_id=to_class_id,
            is_transfer=True,
        )
        
    # Assert
    
    assert e.value.status_code == 404
    assert e.value.detail == ERROR_CHILD_GET_NOT_FOUND
    
    
def test_StudentUseCases_change_class_fail_not_found_class_id(
    db_session: Session,
    mock_student_on_db
):
    
    # Arrange
    
    uc = StudentUseCases(db_session)
    student_cpf = mock_student_on_db.cpf
    to_class_id = "9999999999999999999"
    
    # Act
    
    with raises(HTTPException) as e:
        
        uc.change_class(
            student_cpf=student_cpf,
            to_class_id=to_class_id,
            is_transfer=True,
        )
        
    # Assert
    
    assert e.value.status_code == 404
    assert e.value.detail == ERROR_CLASSES_GET_NOT_FOUND
    
    

def test_StudentUseCases_change_class_fail_transfer_to_same_class(
    db_session: Session,
    mock_student_on_db,
    mock_class_on_db
):
    
    # Arrange
    
    uc = StudentUseCases(db_session)
    student_cpf = mock_student_on_db.cpf
    to_class_id = mock_class_on_db.id
    is_transfer = True
    
    
    # Act
    
    with raises(HTTPException) as e:
        
        uc.change_class(
            student_cpf=student_cpf,
            to_class_id=to_class_id,
            is_transfer=is_transfer,
        )
    
    # Assert
    
    assert e.value.status_code == 409
    assert e.value.detail == ERROR_CHILD_CHANGE_CLASS_STUDENT_ALREADY_ASSOCIATE