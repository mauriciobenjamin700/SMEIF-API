from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import (
    ERROR_CHILD_ADD_NOT_FOUND_PARENT,
    ERROR_CHILD_DELETE_PARENT_LIMIT_REACHED,
    ERROR_CHILD_DELETE_PARENT_NOT_ASSOCIATE_PARENT,
    ERROR_CHILD_GET_NOT_FOUND,
    MESSAGE_CHILD_DELETE_PARENT_SUCCESS
)
from controllers.student import StudentController
from database.models import ChildParentsModel


def test_student_controller_delete_parent_success(
    db_session: Session,
    mock_student_on_db_with_max_parents,
    mock_parent_on_db
):
    
    student = mock_student_on_db_with_max_parents
    parent = mock_parent_on_db
    
    association_begin = db_session.query(ChildParentsModel).filter(
        ChildParentsModel.child_cpf == student.cpf,
        ChildParentsModel.parent_cpf == parent.cpf
    ).first()
    
    response = StudentController(db_session).delete_parent(
        child_cpf=student.cpf,
        parent_cpf=parent.cpf
    )
    
    association_after = db_session.query(ChildParentsModel).filter(
        ChildParentsModel.child_cpf == student.cpf,
        ChildParentsModel.parent_cpf == parent.cpf
    ).first()

    #Assert

    assert association_begin is not None
    assert association_after is None
    assert response.detail == MESSAGE_CHILD_DELETE_PARENT_SUCCESS
    
    
def test_StudentController_delete_parent_fail_no_parent(
    db_session: Session,
    mock_student_on_db
):
    
    # Arrange
    student = mock_student_on_db
    
    # Act
    controller = StudentController(db_session)
    with raises(HTTPException) as e:
        controller.delete_parent(
            child_cpf=student.cpf,
            parent_cpf="12345678901"
        )
        
    assert e.value.status_code == 404
    assert e.value.detail == ERROR_CHILD_ADD_NOT_FOUND_PARENT
    
    
def test_StudentController_delete_parent_fail_no_student(
    db_session: Session,
    mock_parent_on_db,
    mock_student_on_db
):
    
    # Arrange
    student_cpf = "12345678901"
    parent_cpf = mock_parent_on_db.cpf
    
    # Act
    controller = StudentController(db_session)
    with raises(HTTPException) as e:
        controller.delete_parent(
            child_cpf=student_cpf,
            parent_cpf=parent_cpf
        )
        
    assert e.value.status_code == 404
    assert e.value.detail == ERROR_CHILD_GET_NOT_FOUND


def test_StudentController_delete_parent_fail_min_parent(
    db_session: Session,
    mock_student_on_db,
    mock_parent_on_db
):
    
    # Arrange
    student = mock_student_on_db
    parent = mock_parent_on_db
    association = db_session.query(ChildParentsModel).filter(
        ChildParentsModel.child_cpf == student.cpf,
        ChildParentsModel.parent_cpf == parent.cpf
    ).first()

    
    # Act
    controller = StudentController(db_session)
    with raises(HTTPException) as e:
        controller.delete_parent(
            child_cpf=student.cpf,
            parent_cpf=parent.cpf
        )
        
    assert association is not None
    assert e.value.status_code == 409
    assert e.value.detail == ERROR_CHILD_DELETE_PARENT_LIMIT_REACHED


def test_StudentController_delete_parent_fail_another_parent(
    db_session: Session,
    mock_student_on_db_with_max_parents,
    mock_parent_on_db,
    mock_new_parent_on_db
):
    
    # Arrange
    student = mock_student_on_db_with_max_parents
    parent = mock_parent_on_db
    another_parent = mock_new_parent_on_db
    
    association = db_session.query(ChildParentsModel).filter(
        ChildParentsModel.child_cpf == student.cpf,
        ChildParentsModel.parent_cpf == parent.cpf
    ).first()
    
    # Act
    controller = StudentController(db_session)
    with raises(HTTPException) as e:
        controller.delete_parent(
            child_cpf=student.cpf,
            parent_cpf=another_parent.cpf
        )
        
    assert association is not None
    assert e.value.status_code == 404
    assert e.value.detail == ERROR_CHILD_DELETE_PARENT_NOT_ASSOCIATE_PARENT