from fastapi import HTTPException
from pytest import raises


from constants.classes import ERROR_CLASSES_EVENTS_GET_ALL_NOT_FOUND
from useCases.classes import ClassesUseCases
from utils.format import format_date


def test_uc_classes_get_all_events_success(
    db_session,
    mock_class_event_on_db
):
    
    uc = ClassesUseCases(db_session)

    response = uc.get_all_events()

    assert len(response) == 1

    response = response[0]

    assert response.id == mock_class_event_on_db.id
    assert response.class_id == mock_class_event_on_db.class_id
    assert response.disciplines_id[0] == mock_class_event_on_db.discipline_id
    assert response.teacher_id == mock_class_event_on_db.teacher_id
    assert response.start_date == format_date(mock_class_event_on_db.start_date, False) 
    assert response.end_date == format_date(mock_class_event_on_db.end_date, False)
    assert response.recurrences == [
        uc._Model_to_Recurrence(recurrence)
        for recurrence in mock_class_event_on_db.recurrences
    ]
    assert response.teacher_name == mock_class_event_on_db.teacher.user.name
    assert response.discipline_name == mock_class_event_on_db.discipline.name


def test_uc_classes_get_all_events_empty(
    db_session
):
    
    uc = ClassesUseCases(db_session)

    with raises(HTTPException) as exception:
        uc.get_all_events()


    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CLASSES_EVENTS_GET_ALL_NOT_FOUND