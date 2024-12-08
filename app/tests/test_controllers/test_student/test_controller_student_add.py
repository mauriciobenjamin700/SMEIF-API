from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from controllers.student import StudentController
from schemas.child import StudentResponse

# TODO: Bug dos dados do schema no mapeamento

def test_StudentController_add_success(
    db_session: Session,
    mock_StudentRequest
):
    # Arrange
    controller = StudentController(db_session)
    request = mock_StudentRequest

    # Act
    response = controller.add(request)

    # Assert
    assert isinstance(response, StudentResponse)
    assert isinstance(response.matriculation, str)
    assert response.name == request.name
    assert isinstance(response.class_info, str)
    assert isinstance(response.shift, str)