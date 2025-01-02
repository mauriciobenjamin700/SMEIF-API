
from database.models import NoteModel
from constants.note import (
    SUCCESS_NOTE_ADD, 
    SUCCESS_NOTE_DELETE
)
from schemas.note import NoteResponse
from tests.inspect import inspect_note_response_model


def test_route_note_add(api, mock_NoteRequest):
    response = api.post('/note/add', json=mock_NoteRequest.dict())

    assert response.status_code == 201
    assert response.json() == {'detail': SUCCESS_NOTE_ADD}


def test_route_note_get_all(api, mock_note_on_db, db_session):
    response = api.get('/note/list')

    note = NoteResponse(**response.json()[0])

    assert response.status_code == 200
    inspect_note_response_model(db_session,note, mock_note_on_db)


def test_route_note_get_all_with_filters(api, mock_note_on_db_list, db_session):
    response = api.get('/note/list?semester=1&aval_number=1')

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_route_note_update(api, mock_note_on_db, mock_NoteUpdate_points_and_aval_number, db_session):
    response = api.put('/note/update', json=mock_NoteUpdate_points_and_aval_number.dict())

    assert mock_note_on_db.id == mock_NoteUpdate_points_and_aval_number.id

    note = NoteResponse(**response.json())

    assert response.status_code == 200
    assert isinstance(note, NoteResponse)


def test_route_note_delete(api, mock_note_on_db):
    response = api.delete('/note/delete', params={'note_id': mock_note_on_db.id})

    assert response.status_code == 200
    assert response.json() == {'detail': SUCCESS_NOTE_DELETE}