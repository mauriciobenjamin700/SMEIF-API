from fastapi import HTTPException
from pytest import raises


from constants.classes import (
    ERROR_CLASSES_EVENTS_ADD_RECURRENCES_CONFLICT, 
    MESSAGE_CLASS_EVENT_ADD_SUCCESS,
    MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS
)
from useCases.classes import ClassesUseCases
from database.models import RecurrencesModel


def test_uc_classes_add_recurrences_success_two(
    db_session,
    mock_class_event_on_db,
    mock_Recurrences_list
):
    
    uc = ClassesUseCases(db_session)

    response = uc.add_recurrences(
        class_event_id=mock_class_event_on_db.id,
        recurrences=mock_Recurrences_list
    )

    assert response.detail == MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS

    models = db_session.query(RecurrencesModel).filter_by(class_event_id=mock_class_event_on_db.id).all()

    assert len(models) == 3

    add = len(mock_Recurrences_list)

    for recurrence in mock_Recurrences_list:
        
        for model in models:
            if model.day_of_week == recurrence.day_of_week and model.start_time == recurrence.start_time:
                add -= 1

            else:
                print(f"Model: {model.day_of_week}, {model.start_time}, {model.end_time}") 
                print(f"Recurrence: {recurrence.day_of_week}, {recurrence.start_time}, {recurrence.end_time}\n\n")
    
    assert add == 0


def test_uc_classes_add_recurrences_success_one(
    db_session,
    mock_class_event_on_db,
    mock_Recurrences_list
):
    
    uc = ClassesUseCases(db_session)

    response = uc.add_recurrences(
        class_event_id=mock_class_event_on_db.id,
        recurrences=[mock_Recurrences_list[0]]
    )

    assert response.detail == MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS

    models = db_session.query(RecurrencesModel).filter_by(class_event_id=mock_class_event_on_db.id).all()

    assert len(models) == 2

    add = len(mock_Recurrences_list)

    for recurrence in mock_Recurrences_list:
        
        for model in models:
            if model.day_of_week == recurrence.day_of_week and model.start_time == recurrence.start_time:
                add -= 1

            else:
                print(f"Model: {model.day_of_week}, {model.start_time}, {model.end_time}") 
                print(f"Recurrence: {recurrence.day_of_week}, {recurrence.start_time}, {recurrence.end_time}\n\n")
    
    assert add == 1


def test_uc_classes_add_recurrences_fail_conflict(
    db_session,
    mock_class_event_on_db,
    mock_Recurrences_list
):
    
    uc = ClassesUseCases(db_session)

    with raises(HTTPException) as exception:
        uc.add_recurrences(
            class_event_id=mock_class_event_on_db.id,
            recurrences=mock_Recurrences_list + mock_Recurrences_list
        )

    assert exception.value.status_code == 409
    assert exception.value.detail == ERROR_CLASSES_EVENTS_ADD_RECURRENCES_CONFLICT
