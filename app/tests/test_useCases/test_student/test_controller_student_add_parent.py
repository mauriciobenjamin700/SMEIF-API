from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import (
    ERROR_CHILD_ADD_NOT_FOUND_PARENT,
    ERROR_CHILD_ADD_PARENT_ALREADY_ASSOCIATE_PARENT,
    ERROR_CHILD_ADD_PARENT_LIMIT_REACHED,
    ERROR_CHILD_GET_NOT_FOUND,
    ERROR_CHILD_INVALID_FIELD_KINSHIP, 
    MESSAGE_CHILD_ASSOCIATE_PARENT_SUCCESS
)
from useCases.student import StudentUseCases
from database.models import (
    ChildParentsModel,
)
from schemas.base import Kinship


def test_StudentUseCases_add_parent_success(
    db_session: Session,
    mock_student_on_db,
    mock_new_parent_on_db
):
    
    # Arrange 
    
    uc = StudentUseCases(db_session)
    
    # Act
    
    response = uc.add_parent(
        child_cpf=mock_student_on_db.cpf,
        kinship=Kinship.UNCLE.value,
        parent_cpf=mock_new_parent_on_db.cpf
    )
    
    association = db_session.query(ChildParentsModel).filter(
        ChildParentsModel.child_cpf == mock_student_on_db.cpf,
        ChildParentsModel.parent_cpf == mock_new_parent_on_db.cpf
    )
    
    # Assert
    
    assert response.detail == MESSAGE_CHILD_ASSOCIATE_PARENT_SUCCESS
    assert association is not None
    
    
def test_StudentUseCases_add_parent_fail_invalid_kinship(
    db_session: Session,
    mock_student_on_db,
    mock_new_parent_on_db
):
    
    # Arrange 
    
    uc = StudentUseCases(db_session)
    
    # Act
    
    with raises(HTTPException) as exception:
        
        uc.add_parent(
            child_cpf=mock_student_on_db.cpf,
            kinship='invalid_kinship',
            parent_cpf=mock_new_parent_on_db.cpf
        )
    
    # Assert
    
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CHILD_INVALID_FIELD_KINSHIP


def test_StudentUseCases_add_parent_fail_no_parent_in_db(
    db_session: Session,
    mock_student_on_db
):
    
    # Arrange 
    
    uc = StudentUseCases(db_session)
    
    # Act
    
    with raises(HTTPException) as exception:
        
        uc.add_parent(
            child_cpf=mock_student_on_db.cpf,
            kinship=Kinship.UNCLE.value,
            parent_cpf='12345678900'
        )
    
    # Assert
    
    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CHILD_ADD_NOT_FOUND_PARENT
    
    
def test_StudentUseCases_add_parent_fail_child_student_in_db(
    db_session: Session,
    mock_new_parent_on_db
):
    
    # Arrange 
    
    uc = StudentUseCases(db_session)
    
    # Act
    
    with raises(HTTPException) as exception:
        
        uc.add_parent(
            child_cpf='12345678900',
            kinship=Kinship.UNCLE.value,
            parent_cpf=mock_new_parent_on_db.cpf
        )
    
    # Assert
    
    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CHILD_GET_NOT_FOUND


def test_StudentUseCases_add_parent_fail_parent_student_in_db(
    db_session: Session,
    mock_student_on_db
):
    
    # Arrange 
    
    uc = StudentUseCases(db_session)
    
    # Act
    
    with raises(HTTPException) as exception:
        
        uc.add_parent(
            child_cpf=mock_student_on_db.cpf,
            kinship=mock_student_on_db.child_parents[0].kinship,
            parent_cpf=mock_student_on_db.child_parents[0].parent_cpf
        
        )
    # Assert
    
    assert exception.value.status_code == 409
    assert exception.value.detail == ERROR_CHILD_ADD_PARENT_ALREADY_ASSOCIATE_PARENT
    
    
def test_StudentUseCases_add_parent_fail_max_parent(
    db_session: Session,
    mock_student_on_db_with_max_parents,
    mock_new_parent_on_db
):
    
    # Arrange 
    
    uc = StudentUseCases(db_session)
    
    # Act
    
    with raises(HTTPException) as exception:
        
        uc.add_parent(
            child_cpf=mock_student_on_db_with_max_parents.cpf,
            kinship=Kinship.GRANDMOTHER.value,
            parent_cpf=mock_new_parent_on_db.cpf
        
        )
    # Assert
    
    assert exception.value.status_code == 409
    assert exception.value.detail == ERROR_CHILD_ADD_PARENT_LIMIT_REACHED