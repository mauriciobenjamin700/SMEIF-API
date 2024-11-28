from fastapi import HTTPException
from pytest import raises


from constants.disciplines import (
    ERROR_DISCIPLINES_ADD_CONFLICT, 
    MESSAGE_DISCIPLINE_ADD_SUCCESS
)
from controllers.disciplines import DisciplinesController
from schemas.disciplines import DisciplineRequest


def test_controller_disciplines_add_success(db_session, mock_DisciplineRequest):

    request = DisciplineRequest(**mock_DisciplineRequest.dict())

    uc = DisciplinesController(db_session)

    response = uc.add(request)

    assert response.detail == MESSAGE_DISCIPLINE_ADD_SUCCESS


def test_controller_disciplines_add_fail(db_session, mock_DisciplineRequest, mock_discipline_on_db):

    request = DisciplineRequest(**mock_DisciplineRequest.dict())

    uc = DisciplinesController(db_session)

    with raises(HTTPException) as exception:
        uc.add(request)

    assert exception.value.detail == ERROR_DISCIPLINES_ADD_CONFLICT
    assert exception.value.status_code == 409