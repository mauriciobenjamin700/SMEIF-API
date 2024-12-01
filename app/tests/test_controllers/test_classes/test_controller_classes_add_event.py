from fastapi import HTTPException
from pytest import raises


from constants.classes import(
    ERROR_CLASSES_EVENTS_ADD_CONFLICT,
    ERROR_CLASSES_GET_NOT_FOUND,
    MESSAGE_CLASS_EVENT_ADD_SUCCESS
)
from constants.disciplines import ERROR_DISCIPLINES_GET_NOT_FOUND
from constants.teacher import ERROR_TEACHER_GET_NOT_FOUND
from controllers.classes import ClassesController
from database.models import ClassEventModel
from schemas.classes import ClassEventRequest


def test_controller_classes_add_event_success(db_session, mock_ClassEventRequest):

    controller = ClassesController(db_session)

    request = ClassEventRequest(**mock_ClassEventRequest.dict())

    response = controller.add_event(request)

    assert response.detail == MESSAGE_CLASS_EVENT_ADD_SUCCESS

    model = db_session.query(ClassEventModel).filter(ClassEventModel.class_id == request.class_id).first()

    assert request.class_id == model.class_id
    assert model.discipline_id == model.discipline_id
    assert model.teacher_id == model.teacher_id
    assert model.start_date == model.start_date
    assert model.end_date == model.end_date


def test_controller_classes_add_event_fail_conflict(
        db_session, 
        mock_ClassEventRequest, 
        mock_class_event_on_db
):

    controller = ClassesController(db_session)

    request = ClassEventRequest(**mock_ClassEventRequest.dict())

    with raises(HTTPException) as exception:
        controller.add_event(request)

    assert exception.value.status_code == 409
    assert exception.value.detail == ERROR_CLASSES_EVENTS_ADD_CONFLICT


def test_controller_classes_add_event_fail_class_not_found(
        db_session, 
        mock_ClassEventRequest
):

    controller = ClassesController(db_session)

    request = ClassEventRequest(**mock_ClassEventRequest.dict())

    request.class_id = "invalid_id"

    with raises(HTTPException) as exception:
        controller.add_event(request)

    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CLASSES_GET_NOT_FOUND


def test_controller_classes_add_event_fail_discipline_not_found_discipline(
        db_session, 
        mock_ClassEventRequest
):

    controller = ClassesController(db_session)

    request = ClassEventRequest(**mock_ClassEventRequest.dict())

    request.disciplines_id = ["invalid_id"]

    with raises(HTTPException) as exception:
        controller.add_event(request)

    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_DISCIPLINES_GET_NOT_FOUND


def test_controller_classes_add_event_fail_discipline_not_found_disciplines(
        db_session, 
        mock_ClassEventRequest
):

    controller = ClassesController(db_session)

    request = ClassEventRequest(**mock_ClassEventRequest.dict())

    request.disciplines_id += ["invalid_id"]

    with raises(HTTPException) as exception:
        controller.add_event(request)

    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_DISCIPLINES_GET_NOT_FOUND


def test_controller_classes_add_event_fail_teacher_not_found(
        db_session, 
        mock_ClassEventRequest
):

    controller = ClassesController(db_session)

    request = ClassEventRequest(**mock_ClassEventRequest.dict())

    request.teacher_id = "invalid_id"

    with raises(HTTPException) as exception:
        controller.add_event(request)

    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_TEACHER_GET_NOT_FOUND
