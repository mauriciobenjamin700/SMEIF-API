from constants.classes import (
    MESSAGE_CLASS_ADD_SUCCESS,
    MESSAGE_CLASS_DELETE_SUCCESS,
    MESSAGE_CLASS_EVENT_ADD_SUCCESS,
    MESSAGE_CLASS_EVENT_DELETE_SUCCESS,
    MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS,
    MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS
)
from schemas.classes import (
    ClassEventResponse, 
    ClassResponse,
    Recurrences
)
from utils.format import format_date


def test_route_classes_add(api, mock_ClassRequest):

    request = mock_ClassRequest.dict()

    response = api.post("/classes/add", json=request)

    assert response.status_code == 201
    assert response.json() == {"detail": MESSAGE_CLASS_ADD_SUCCESS}


def test_route_classes_get(api, mock_class_on_db):

    response = api.get(f"/classes/get?class_id={mock_class_on_db.id}")

    data = ClassResponse(**response.json())

    assert response.status_code == 200
    assert data.id == mock_class_on_db.id
    assert data.name == mock_class_on_db.name
    assert data.education_level == mock_class_on_db.education_level
    assert data.section == mock_class_on_db.section
    assert data.shift == mock_class_on_db.shift
    assert data.max_students == mock_class_on_db.max_students


def test_route_classes_list(api, mock_class_on_db):
    
        response = api.get("/classes/list")
    
        data = [ClassResponse(**item) for item in response.json()]
    
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0].id == mock_class_on_db.id
        assert data[0].name == mock_class_on_db.name
        assert data[0].education_level == mock_class_on_db.education_level
        assert data[0].section == mock_class_on_db.section
        assert data[0].shift == mock_class_on_db.shift
        assert data[0].max_students == mock_class_on_db.max_students


def test_route_classes_update(api, mock_class_on_db, mock_ClassRequest):
         
    request = mock_ClassRequest.dict()

    response = api.put(f"/classes/update?class_id={mock_class_on_db.id}", json=request)

    data = ClassResponse(**response.json())

    assert response.status_code == 200
    assert data.id == mock_class_on_db.id
    assert data.name == mock_ClassRequest.name
    assert data.education_level == mock_ClassRequest.education_level
    assert data.section == mock_ClassRequest.section
    assert data.shift == mock_ClassRequest.shift
    assert data.max_students == mock_ClassRequest.max_students


def test_route_classes_delete(api, mock_class_on_db):
         
    response = api.delete(f"/classes/delete?class_id={mock_class_on_db.id}")

    assert response.status_code == 200
    assert response.json() == {"detail": MESSAGE_CLASS_DELETE_SUCCESS}


def test_route_classes_add_event(api, mock_ClassEventRequest):

    request = mock_ClassEventRequest.dict()

    response = api.post("/classes/add-event", json=request)

    assert response.status_code == 201
    assert response.json() == {"detail": MESSAGE_CLASS_EVENT_ADD_SUCCESS}


def test_route_classes_get_event(api, mock_class_event_on_db):

    response = api.get(f"/classes/get-event?class_event_id={mock_class_event_on_db.id}")

    assert response.status_code == 200

    print(response.json())

    data = ClassEventResponse(**response.json())

    assert response.status_code == 200
    assert data.id == mock_class_event_on_db.id
    assert data.class_id == mock_class_event_on_db.class_id
    assert data.disciplines_id == [mock_class_event_on_db.discipline_id]
    assert data.start_date == format_date(mock_class_event_on_db.start_date, False)
    assert data.end_date == format_date(mock_class_event_on_db.end_date, False) 


def test_route_classes_list_events(api, mock_class_event_on_db):
    
    response = api.get("/classes/list-events")
    
    data = [ClassEventResponse(**item) for item in response.json()]
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0].id == mock_class_event_on_db.id
    assert data[0].class_id == mock_class_event_on_db.class_id
    assert data[0].disciplines_id == [mock_class_event_on_db.discipline_id]
    assert data[0].start_date == format_date(mock_class_event_on_db.start_date, False)
    assert data[0].end_date == format_date(mock_class_event_on_db.end_date, False)


def test_route_classes_update_event(api, mock_class_event_on_db, mock_ClassEventUpdate):
         
    request = mock_ClassEventUpdate.dict()

    response = api.put(f"/classes/update-event?class_event_id={mock_class_event_on_db.id}", json=request)

    data = ClassEventResponse(**response.json())

    assert response.status_code == 200
    assert data.id == mock_class_event_on_db.id
    assert data.class_id == mock_ClassEventUpdate.class_id
    assert data.disciplines_id == mock_ClassEventUpdate.disciplines_id
    assert data.start_date == mock_ClassEventUpdate.start_date
    assert data.end_date == mock_ClassEventUpdate.end_date


def test_route_classes_delete_event(api, mock_class_event_on_db):
             
        response = api.delete(f"/classes/delete-event?class_event_id={mock_class_event_on_db.id}")
    
        assert response.status_code == 200
        assert response.json() == {"detail": MESSAGE_CLASS_EVENT_DELETE_SUCCESS}


def test_route_classes_add_recurrences(api, mock_class_event_on_db, mock_Recurrences_list):
     
    request = [recurrence.dict() for recurrence in mock_Recurrences_list]

    response = api.post(f"/classes/add-recurrences?class_event_id={mock_class_event_on_db.id}", json=request)

    assert response.status_code == 201
    assert response.json() == {"detail": MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS}


def test_route_classes_delete_recurrences(api, mock_class_event_on_db, mock_recurrence_on_db):

    request = [Recurrences(**mock_recurrence_on_db.dict()).dict()]
             
    response = api.put(f"/classes/delete-recurrences?class_event_id={mock_class_event_on_db.id}", json=request)
    
    assert response.status_code == 200
    assert response.json() == {"detail": MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS}