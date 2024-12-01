from fastapi import HTTPException
from pytest import raises


from constants.classes import (
    ERROR_CLASS_ADD_CONFLICT,
    MESSAGE_CLASS_ADD_SUCCESS
)
from controllers.classes import ClassesController
from database.queries.get import get_class_by_name
from schemas.classes import (
    ClassRequest
)


def test_controller_classes_add_success(db_session, mock_ClassRequest):

    uc = ClassesController(db_session)

    request = ClassRequest(**mock_ClassRequest.dict())

    response = uc.add(request)

    assert response.detail == MESSAGE_CLASS_ADD_SUCCESS

    model = get_class_by_name(db_session, request.name)

    assert model.education_level == request.education_level
    assert model.name == request.name
    assert model.section == request.section
    assert model.shift == request.shift
    assert model.max_students == request.max_students


def test_controller_classes_add_conflict(db_session, mock_ClassRequest):

    uc = ClassesController(db_session)

    request = ClassRequest(**mock_ClassRequest.dict())

    with raises(HTTPException) as exception:
        uc.add(request)
        uc.add(request)

    assert exception.value.status_code == 409
    assert exception.value.detail == ERROR_CLASS_ADD_CONFLICT