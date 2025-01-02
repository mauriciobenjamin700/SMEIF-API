from fastapi import HTTPException
from sqlalchemy.orm import Session
from pytest import raises


from constants.note import ERROR_NOTE_NOT_FOUND_NOTES
from database.models import NoteModel
from schemas.note import (
    NoteFilters, 
    NoteResponse
)
from tests.inspect import inspect_note_response_model
from useCases.note import NoteUseCases


def test_NoteUseCases_get_all_success(
    db_session: Session,
    mock_note_on_db: NoteModel
):
    
    # Arrange
    use_case = NoteUseCases(db_session)
    
    # Act
    result = use_case.get_all()
    
    # Assert
    assert isinstance(result, list)
    assert isinstance(result[0], NoteResponse)
    assert len(result) == 1
    inspect_note_response_model(
        db_session,
        result[0],
        mock_note_on_db
    )


def test_NoteUseCases_get_all_empty(
    db_session: Session
):
    
    # Arrange
    use_case = NoteUseCases(db_session)
    
    # Act
    with raises(HTTPException) as e:
        use_case.get_all()
    
    # Assert
    assert e.value.status_code == 404
    assert e.value.detail == ERROR_NOTE_NOT_FOUND_NOTES


def test_NoteUseCases_get_all_with_filters_success_1_semester(
    db_session: Session,
    mock_note_on_db_list: list[NoteModel]
):
    
    # Arrange
    use_case = NoteUseCases(db_session)

    filters = NoteFilters(
        semester=1
    )
    
    # Act

    response = use_case.get_all(filters=filters)

    # Assert

    assert len(response) == 4

    for note in response:
        assert note.semester == 1
    

def test_NoteUseCases_get_all_with_filters_success_2_semester(
    db_session: Session,
    mock_note_on_db_list: list[NoteModel]
):
    
    # Arrange
    use_case = NoteUseCases(db_session)

    filters = NoteFilters(
        semester=2
    )
    
    # Act

    response = use_case.get_all(filters=filters)

    # Assert

    assert len(response) == 1

    for note in response:
        assert note.semester == 2


def test_NoteUseCases_get_all_with_filters_success_1_aval_number(
    db_session: Session,
    mock_note_on_db_list: list[NoteModel]
):
    
    # Arrange
    use_case = NoteUseCases(db_session)

    filters = NoteFilters(
        aval_number=1
    )

    # Act

    response = use_case.get_all(filters=filters)

    # Assert

    assert len(response) == 2

    for note in response:
        assert note.aval_number == 1


def test_NoteUseCases_get_all_with_filters_success_1_aval_number_1_semester(
    db_session: Session,
    mock_note_on_db_list: list[NoteModel]
):
    
    # Arrange
    use_case = NoteUseCases(db_session)

    filters = NoteFilters(
        semester=1,
        aval_number=1
    )

    # Act

    response = use_case.get_all(filters=filters)

    # Assert

    assert len(response) == 1

    for note in response:
        assert note.semester == 1
        assert note.aval_number == 1


# TODO: Seria bom testar todos os casos de filtros, mas por hora foi so dois mesmo