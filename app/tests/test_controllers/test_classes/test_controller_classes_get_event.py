from fastapi import HTTPException
from pytest import raises


from constants.classes import ERROR_CLASSES_EVENTS_GET_NOT_FOUND
from controllers.classes import ClassesController
from utils.format import format_date


def test_controller_classes_get_event_success(
    db_session,
    mock_class_event_on_db
):
    
    controller = ClassesController(db_session)

    response = controller.get_event(class_event_id=mock_class_event_on_db.id)


    assert response.id == mock_class_event_on_db.id
    assert response.class_id == mock_class_event_on_db.class_id
    assert response.disciplines_id[0] == mock_class_event_on_db.discipline_id
    assert response.teacher_id == mock_class_event_on_db.teacher_id
    assert response.start_date == format_date(mock_class_event_on_db.start_date, False) 
    assert response.end_date == format_date(mock_class_event_on_db.end_date, False)
    assert response.recurrences == [
        controller._Model_to_Recurrence(recurrence)
        for recurrence in mock_class_event_on_db.recurrences
    ]
    assert response.teacher_name == mock_class_event_on_db.teacher.user.name
    assert response.discipline_name == mock_class_event_on_db.discipline.name


def test_controller_classes_get_event_not_found(
    db_session
):
    
    controller = ClassesController(db_session)

    with raises(HTTPException) as exception:
        controller.get_event(class_event_id="not_found")

    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CLASSES_EVENTS_GET_NOT_FOUND
