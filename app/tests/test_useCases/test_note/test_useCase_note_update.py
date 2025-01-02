from fastapi import HTTPException
from pytest import raises


from constants.note import ERROR_NOTE_NOT_FOUND
from tests.inspect import inspect_note_response_model
from useCases.note import NoteUseCases


def test_NoteUseCases_update_success(
    db_session,
    mock_note_on_db,
    mock_NoteUpdate_points_and_aval_number,
):
    # Arrange
    use_case = NoteUseCases(db_session)
    request = mock_NoteUpdate_points_and_aval_number
    
    # Act
    response = use_case.update(request)
    
    # Assert
    inspect_note_response_model(
        db_session=db_session,
        response=response,
        model=mock_note_on_db
    )
    

def test_NoteUseCases_update_note_not_found(
    db_session,
    mock_NoteUpdate_points_and_aval_number,
):
    # Arrange
    use_case = NoteUseCases(db_session)
    request = mock_NoteUpdate_points_and_aval_number
    request.id = "9999"
    
    # Act
    with raises(HTTPException) as exception:
        use_case.update(request)
    
    # Assert
    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_NOTE_NOT_FOUND
    

def test_NoteUseCases_update_note_success_aval_number(
    db_session,
    mock_note_on_db,
    mock_NoteUpdate_aval_number,
):
    
    # Arrange
    use_case = NoteUseCases(db_session)

    request = mock_NoteUpdate_aval_number

    # Act
    response = use_case.update(request)

    # Assert
    inspect_note_response_model(
        db_session=db_session,
        response=response,
        model=mock_note_on_db
    )


def test_NoteUseCases_update_note_success_points(
    db_session,
    mock_note_on_db,
    mock_NoteUpdate_points,
):
    
    # Arrange
    use_case = NoteUseCases(db_session)

    request = mock_NoteUpdate_points

    # Act
    response = use_case.update(request)

    # Assert
    inspect_note_response_model(
        db_session=db_session,
        response=response,
        model=mock_note_on_db
    )