from fastapi import HTTPException
from pytest import raises


from constants.base import ERROR_INVALID_CPF
from constants.note import(
    ERROR_NOTE_INVALID_FIELD_AVAL_NUMBER,
    ERROR_NOTE_REQUIRED_FIELD_AVAL_NUMBER,
    ERROR_NOTE_REQUIRED_FIELD_POINTS,
    ERROR_NOTE_REQUIRED_FIELD_DISCIPLINES_ID,
    ERROR_NOTE_REQUIRED_FIELD_CLASS_ID,
    ERROR_NOTE_REQUIRED_FIELD_CHILD_CPF,
    ERROR_NOTE_INVALID_FIELD_POINTS,
    ERROR_NOTE_REQUIRED_FIELD_SEMESTER,
)
from schemas.note import(
    NoteDB,
    NoteFilters,
    NoteRequest
)
from utils.format import unformat_cpf


def test_NoteRequest_success(
    mock_NoteRequest_data
):
    data = mock_NoteRequest_data
    
    request = NoteRequest(**data)
    
    
    assert request.semester == data["semester"]
    assert request.aval_number == data["aval_number"]
    assert request.discipline_id == data["discipline_id"]
    assert request.class_id == data["class_id"]
    assert request.child_cpf == unformat_cpf(data["child_cpf"])
    
    
def test_NoteRequest_fail_no_semester(
    mock_NoteRequest_data
):
    
    data = mock_NoteRequest_data
    data["semester"] = None
    
    with raises(HTTPException) as exception:
        NoteRequest(**data)
        
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_REQUIRED_FIELD_SEMESTER



def test_NoteRequest_fail_invalid_semester(
    mock_NoteRequest_data
):
    
    data = mock_NoteRequest_data
    data["semester"] = 22
    
    with raises(HTTPException) as exception:
        NoteRequest(**data)
        
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_INVALID_FIELD_POINTS


def test_NoteRequest_fail_no_aval_number(
    mock_NoteRequest_data
):
    
    data = mock_NoteRequest_data
    data["aval_number"] = None
    
    with raises(HTTPException) as exception:
        NoteRequest(**data)
        
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_REQUIRED_FIELD_AVAL_NUMBER


def test_NoteRequest_fail_invalid_aval_number(
    mock_NoteRequest_data
):
    
    data = mock_NoteRequest_data
    data["aval_number"] = 22
    
    with raises(HTTPException) as exception:
        NoteRequest(**data)
        
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_INVALID_FIELD_AVAL_NUMBER


def test_NoteRequest_fail_no_points(
    mock_NoteRequest_data
):

    data = mock_NoteRequest_data
    data["points"] = None

    with raises(HTTPException) as exception:
        NoteRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_REQUIRED_FIELD_POINTS



def test_NoteRequest_fail_invalid_points(
    mock_NoteRequest_data
):

    data = mock_NoteRequest_data
    data["points"] = 101

    with raises(HTTPException) as exception:
        NoteRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_INVALID_FIELD_POINTS


def test_NoteRequest_fail_no_discipline_id(
    mock_NoteRequest_data
):

    data = mock_NoteRequest_data
    data["discipline_id"] = None

    with raises(HTTPException) as exception:
        NoteRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_REQUIRED_FIELD_DISCIPLINES_ID


def test_NoteRequest_fail_no_class_id(
    mock_NoteRequest_data
):

    data = mock_NoteRequest_data
    data["class_id"] = None

    with raises(HTTPException) as exception:
        NoteRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_REQUIRED_FIELD_CLASS_ID


def test_NoteRequest_fail_no_child_cpf(
    mock_NoteRequest_data
):

    data = mock_NoteRequest_data
    data["child_cpf"] = None

    with raises(HTTPException) as exception:
        NoteRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_NOTE_REQUIRED_FIELD_CHILD_CPF


def test_NoteRequest_fail_invalid_child_cpf(
    mock_NoteRequest_data
):

    data = mock_NoteRequest_data
    data["child_cpf"] = "123.456.789-0"

    with raises(HTTPException) as exception:
        NoteRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_INVALID_CPF


def test_NoteDB_success(
    mock_NoteRequest_data
):
    data = mock_NoteRequest_data
    
    request = NoteRequest(**data)
    
    db = NoteDB(**request.dict())
    
    assert db.semester == data["semester"]
    assert db.aval_number == data["aval_number"]
    assert db.discipline_id == data["discipline_id"]
    assert db.class_id == data["class_id"]
    assert db.child_cpf == unformat_cpf(data["child_cpf"])
    assert db.id is not None


def test_NoteFilters_success(
    mock_NoteFilters_data
):
    
    data = mock_NoteFilters_data

    filters = NoteFilters(**data)

    assert filters.semester == data["semester"]
    assert filters.aval_number == data["aval_number"]
    assert filters.discipline_id == data["discipline_id"]
    assert filters.class_id == data["class_id"]
    assert filters.child_cpf == unformat_cpf(data["child_cpf"])
    


def test_NoteFilters_invalid_cpf(
    mock_NoteFilters_data
):
    
    data = mock_NoteFilters_data

    data["child_cpf"] = "123.456.789-0"

    with raises(HTTPException) as e:
        NoteFilters(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF