from constants.classes import MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS
from controllers.classes import ClassesController
from database.models import RecurrencesModel


def test_controller_classes_delete_recurrences_success_one(
    db_session,
    mock_class_event_on_db,
    mock_ClassEventRequest
):
    

    controller = ClassesController(db_session)

    recurrences = mock_ClassEventRequest.recurrences

    assert len(recurrences) == 1


    response = controller.delete_recurrences(
        class_event_id=mock_class_event_on_db.id,
        recurrences=recurrences
    )

    assert response.detail == MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS

    models = db_session.query(RecurrencesModel).filter_by(class_event_id=mock_class_event_on_db.id).first()

    assert models is None


def test_controller_classes_delete_recurrences_success_two(
    db_session,
    mock_class_event_on_db,
    mock_ClassEventRequest,
    mock_recurrence_on_db
):
    

    controller = ClassesController(db_session)

    recurrences = mock_ClassEventRequest.recurrences

    assert len(mock_class_event_on_db.recurrences) == 2


    response = controller.delete_recurrences(
        class_event_id=mock_class_event_on_db.id,
        recurrences=recurrences + [controller._Model_to_Recurrence(mock_recurrence_on_db)]
    )

    assert response.detail == MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS

    models = db_session.query(RecurrencesModel).filter_by(class_event_id=mock_class_event_on_db.id).all()

    assert not models


