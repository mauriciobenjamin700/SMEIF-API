from fastapi import HTTPException
from pytest import raises
from sqlalchemy.orm import Session


from constants.child import ERROR_CHILD_GET_NOT_FOUND
from constants.classes import ERROR_CLASSES_GET_NOT_FOUND
from constants.disciplines import ERROR_DISCIPLINES_GET_NOT_FOUND
from constants.note import (
    ERROR_NOTE_ALREADY_ADD
)
from database.models import NoteModel
from database.repositories.note import NoteRepository

def inspect_notes_model(Note1: NoteModel, note2: NoteModel):
    assert Note1.id == note2.id
    assert Note1.child_cpf == note2.child_cpf
    assert Note1.discipline_id == note2.discipline_id
    assert Note1.class_id == note2.class_id
    assert Note1.aval_number == note2.aval_number
    assert Note1.semester == note2.semester


def test_NoteRepository_add_success(
    db_session: Session,
    mock_NoteRequest
):
    
    request  = mock_NoteRequest

    repository = NoteRepository(db_session)

    model = repository.map_request_to_model(request)

    repository.add(model)

    on_db = repository.get(model.id)

    inspect_notes_model(model, on_db)


def test_NoteRepository_get_success(
    db_session: Session,
    mock_note_on_db
):
    model = mock_note_on_db

    db_session.add(model)
    db_session.commit()

    repository = NoteRepository(db_session)

    on_db = repository.get(model.id)

    inspect_notes_model(model, on_db)


def test_NoteRepository_get_not_found(
    db_session: Session
):
    repository = NoteRepository(db_session)

    on_db = repository.get("123")

    assert on_db is None


def test_NoteRepository_get_by_child_cpf_success(
    db_session: Session,
    mock_note_on_db
):
    model = mock_note_on_db

    db_session.add(model)
    db_session.commit()

    repository = NoteRepository(db_session)

    on_db = repository.get_by_child_cpf(model.child_cpf)
    assert len(on_db) == 1
    inspect_notes_model(model, on_db[0])


def test_NoteRepository_get_by_child_cpf_not_found(
    db_session: Session
):
    repository = NoteRepository(db_session)

    on_db = repository.get_by_child_cpf("123")

    assert on_db == []


def test_NoteRepository_get_all_success(
    db_session: Session,
    mock_note_on_db
):
    model = mock_note_on_db

    db_session.add(model)
    db_session.commit()

    repository = NoteRepository(db_session)

    on_db = repository.get_all()
    assert len(on_db) == 1
    inspect_notes_model(model, on_db[0])



def test_NoteRepository_update_success(
    db_session: Session,
    mock_note_on_db
):
    model = mock_note_on_db

    db_session.add(model)
    db_session.commit()

    repository = NoteRepository(db_session)

    model.aval_number = 10

    updated = repository.update(model)

    inspect_notes_model(model, updated)


def test_NoteRepository_delete_success(
    db_session: Session,
    mock_note_on_db
):
    model = mock_note_on_db

    db_session.add(model)
    db_session.commit()

    repository = NoteRepository(db_session)

    result = repository.delete(model.id)

    assert result == True
    assert repository.get(model.id) is None


def test_NoteRepository_delete_not_found(
    db_session: Session
):
    repository = NoteRepository(db_session)

    result = repository.delete("123")

    assert result == False


def test_NoteRepository_map_model_to_response(
    db_session: Session,
    mock_student_on_db,
    mock_discipline_on_db,
    mock_class_on_db,
    mock_note_on_db
):
    model = mock_note_on_db

    repository = NoteRepository(db_session)

    response = repository.map_model_to_response(model)

    assert response.id == model.id
    assert response.aval_number == model.aval_number
    assert response.semester == model.semester
    assert response.child_cpf == mock_student_on_db.cpf
    assert response.discipline_id == mock_discipline_on_db.id
    assert response.class_id == mock_class_on_db.id
    assert response.student_name == mock_student_on_db.name
    assert response.discipline_name == mock_discipline_on_db.name
    assert response.class_name == mock_class_on_db.name
    assert response.class_shift == mock_class_on_db.shift


def test_NoteRepository_validate_note(
    db_session: Session,
    mock_NoteRequest
):
    
    request  = mock_NoteRequest

    repository = NoteRepository(db_session)

    response = repository.validate_note(request)

    assert response is None


def test_NoteRepository_validate_note_already_exists(
    db_session: Session,
    mock_note_on_db,
    mock_NoteRequest
):
    
    request  = mock_NoteRequest
    

    repository = NoteRepository(db_session)

    with raises(HTTPException) as e:

        repository.validate_note(request)

    
    assert e.value.status_code == 409
    assert e.value.detail == ERROR_NOTE_ALREADY_ADD


def test_NoteRepository_validate_note_not_found_discipline_id(
    db_session: Session,
    mock_NoteRequest
):
    
    request = mock_NoteRequest
    request.discipline_id = "123"

    repository = NoteRepository(db_session)

    with raises(HTTPException) as e:
        repository.validate_note(request)

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DISCIPLINES_GET_NOT_FOUND


def test_NoteRepository_validate_note_not_found_class_id(
    db_session: Session,
    mock_NoteRequest
):
    
    request = mock_NoteRequest
    request.class_id = "123"

    repository = NoteRepository(db_session)

    with raises(HTTPException) as e:
        repository.validate_note(request)

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_CLASSES_GET_NOT_FOUND


def test_NoteRepository_validate_note_not_found_student_cpf(
    db_session: Session,
    mock_NoteRequest
):
    
    request = mock_NoteRequest
    request.child_cpf = "123"

    repository = NoteRepository(db_session)

    with raises(HTTPException) as e:
        repository.validate_note(request)

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_CHILD_GET_NOT_FOUND