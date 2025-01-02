from datetime import datetime
from fastapi import HTTPException
from pytest import raises


from constants.base import ERROR_INVALID_CPF
from constants.child import ERROR_CHILD_REQUIRED_FIELD_CPF

from constants.presence import(
    ERROR_PRESENCE_INVALID_FIELD_TYPE,
    ERROR_PRESENCE_REQUIRED_FIELD_CLASS_EVENT_ID,
    ERROR_PRESENCE_REQUIRED_FIELD_TYPE
)
from schemas.presence import (
    PresenceRequest,
    PresenceDB
)
from utils.format import unformat_cpf

def test_PresenceRequest_success(
    mock_PresenceRequest_data
):
    
    data = mock_PresenceRequest_data.copy()
    
    request = PresenceRequest(**data)

    assert request.class_event_id == data["class_event_id"]
    assert request.child_cpf == unformat_cpf(data["child_cpf"])
    assert request.type == data["type"]


def test_PresenceRequest_fail_no_class_event_id(
    mock_PresenceRequest_data
):
    
    data = mock_PresenceRequest_data.copy()
    del data["class_event_id"]
    
    with raises(HTTPException) as exception:
        PresenceRequest(**data)
    
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_PRESENCE_REQUIRED_FIELD_CLASS_EVENT_ID


def test_PresenceRequest_fail_no_child_cpf(
    mock_PresenceRequest_data
):
    data = mock_PresenceRequest_data.copy()
    del data["child_cpf"]

    with raises(HTTPException) as exception:
        PresenceRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CHILD_REQUIRED_FIELD_CPF


def test_PresenceRequest_fail_invalid_child_cpf(
    mock_PresenceRequest_data
):
    
    data = mock_PresenceRequest_data.copy()
    data["child_cpf"] = "123.456.789-0"
    
    with raises(HTTPException) as exception:
        PresenceRequest(**data)
    
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_INVALID_CPF


def test_PresenceRequest_fail_no_type(
    mock_PresenceRequest_data
):
    
    data = mock_PresenceRequest_data.copy()
    del data["type"]
    
    with raises(HTTPException) as exception:
        PresenceRequest(**data)
    
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_PRESENCE_REQUIRED_FIELD_TYPE


def test_PresenceRequest_fail_invalid_type(
    mock_PresenceRequest_data
):
    
    data = mock_PresenceRequest_data.copy()
    data["type"] = "X"
    
    with raises(HTTPException) as exception:
        PresenceRequest(**data)
    
    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_PRESENCE_INVALID_FIELD_TYPE


def test_PresenceDB_success(
    mock_PresenceRequest_data
):
    
    data = mock_PresenceRequest_data.copy()
    
    db = PresenceDB(**data)

    assert db.class_event_id == data["class_event_id"]
    assert db.child_cpf == unformat_cpf(data["child_cpf"])
    assert db.type == data["type"]
    assert isinstance(db.created_at, datetime)
    assert isinstance(db.id, str)