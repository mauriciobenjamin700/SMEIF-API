from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import MESSAGE_CHILD_ASSOCIATE_PARENT_SUCCESS
from controllers.student import StudentController
from database.models import (
    ChildParentsModel,
)
from schemas.base import Kinship


def test_StudentController_add_parent_success(
    db_session: Session,
    mock_student_on_db,
    mock_new_parent_on_db
):
    
    # Arrange 
    
    controller = StudentController(db_session)
    
    # Act
    
    response = controller.add_parent(
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