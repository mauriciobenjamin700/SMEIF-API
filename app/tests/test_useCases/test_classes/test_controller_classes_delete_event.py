from fastapi import HTTPException
from pytest import raises


from constants.classes import MESSAGE_CLASS_EVENT_DELETE_SUCCESS
from useCases.classes import ClassesUseCases
from database.models import ClassEventModel


def test_uc_classes_delete_event(
    db_session, 
    mock_class_event_on_db,
):
    
    uc = ClassesUseCases(db_session)

    response = uc.delete_event(mock_class_event_on_db.id)

    assert response.detail == MESSAGE_CLASS_EVENT_DELETE_SUCCESS

    model = db_session.query(ClassEventModel).filter(ClassEventModel.id == mock_class_event_on_db.id).first()

    assert model is None