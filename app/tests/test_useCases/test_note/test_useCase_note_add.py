from sqlalchemy.orm import Session


from constants.note import (
    SUCCESS_NOTE_ADD
)
from database.models import (
    NoteModel
)
from schemas.note  import (
    NoteRequest,
    NoteResponse
)
from useCases.note import NoteUseCases


def test_NoteUseCases_add_success(
    db_session: Session,
    mock_NoteRequest: NoteRequest
):
    # Arrange
    use_case = NoteUseCases(db_session)
    request = NoteRequest(**mock_NoteRequest.dict())
    
    # Act
    response = use_case.add(request)
    db = db_session.query(NoteModel).filter(
        NoteModel.discipline_id == request.discipline_id,
        NoteModel.teacher_id == request.teacher_id,
        NoteModel.child_cpf == request.child_cpf,
    ).first()
    
    # Assert
    response.detail == SUCCESS_NOTE_ADD
    assert db is not None

