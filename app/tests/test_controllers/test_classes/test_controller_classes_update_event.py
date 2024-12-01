from controllers.classes import ClassesController
from schemas.classes import ClassEventRequest


def test_controller_classes_update_event_success(
    db_session, 
    mock_ClassEventUpdate,
    mock_class_event_on_db,
):
    
    controller = ClassesController(db_session)

    request = ClassEventRequest(**mock_ClassEventUpdate.dict())

    response = controller.update_event(
        mock_class_event_on_db.id,
        request
    )

    assert response.id == mock_class_event_on_db.id
    assert response.class_id == request.class_id
    assert response.disciplines_id[0] == request.disciplines_id[0]
    assert response.teacher_id == request.teacher_id
    assert response.start_date == request.start_date
    assert response.end_date == request.end_date
    assert response.recurrences == [
        controller._Model_to_Recurrence(recurrence)
        for recurrence in mock_class_event_on_db.recurrences
    ]
    assert response.teacher_name == mock_class_event_on_db.teacher.user.name
    assert response.discipline_name == mock_class_event_on_db.discipline.name
