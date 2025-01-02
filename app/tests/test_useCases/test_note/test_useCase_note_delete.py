from fastapi import HTTPException
from sqlalchemy.orm import Session
from pytest import raises


from constants.note import (
    ERROR_NOTE_NOT_FOUND,
    SUCCESS_NOTE_DELETE
)
from database.models import NoteModel
from useCases.note import NoteUseCases


def test_NoteUseCases_delete_success(
    db_session: Session,
    mock_note_on_db: NoteModel
):
    
    uc = NoteUseCases(db_session)
    idx = mock_note_on_db.id

    response = uc.delete(idx)
    model = db_session.query(NoteModel).get(idx)

    assert response.detail == SUCCESS_NOTE_DELETE
    assert model is None


def test_NoteUseCases_delete_not_found(
    db_session: Session
):
    
    uc = NoteUseCases(db_session)
    idx = "1"

    with raises(HTTPException) as exception:
        uc.delete(idx)

    assert exception.value.detail == ERROR_NOTE_NOT_FOUND
    assert exception.value.status_code == 404
