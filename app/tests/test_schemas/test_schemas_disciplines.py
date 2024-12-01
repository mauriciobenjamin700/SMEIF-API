from fastapi import HTTPException
from pytest import raises


from constants.disciplines import (
    ERROR_DISCIPLINES_REQUIRED_FIELD_NAME
)
from schemas.disciplines import(
    DisciplineRequest,
    DisciplineResponse
)


def test_DisciplineRequest_success(mock_discipline_request_data):

    discipline_request = DisciplineRequest(**mock_discipline_request_data)

    assert discipline_request.name == mock_discipline_request_data["name"]


def test_DisciplineRequest_fail(mock_discipline_request_data):

    mock_discipline_request_data["name"] = "   "

    with raises(HTTPException) as e:
        DisciplineRequest(**mock_discipline_request_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_DISCIPLINES_REQUIRED_FIELD_NAME


def test_DisciplineResponse_success(mock_discipline_response_data):

    discipline_response = DisciplineResponse(**mock_discipline_response_data)

    assert discipline_response.id == mock_discipline_response_data["id"]
    assert discipline_response.name == mock_discipline_response_data["name"]