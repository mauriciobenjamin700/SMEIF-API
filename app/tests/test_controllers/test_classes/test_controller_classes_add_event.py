from fastapi import HTTPException
from pytest import raises


from constants.classes import(
    MESSAGE_CLASS_EVENT_ADD_SUCCESS
)
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

