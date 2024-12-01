from fastapi import HTTPException
from pytest import raises


from constants.classes import MESSAGE_CLASS_EVENT_DELETE_SUCCESS
from controllers.classes import ClassesController
from database.models import ClassEventModel


def test_controller_classes_delete_event(
    db_session, 
    mock_class_event_on_db,
):
    
    controller = ClassesController(db_session)

    response = controller.delete_event(mock_class_event_on_db.id)

    assert response.detail == MESSAGE_CLASS_EVENT_DELETE_SUCCESS

    model = db_session.query(ClassEventModel).filter(ClassEventModel.id == mock_class_event_on_db.id).first()

    assert model is None