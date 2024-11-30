from fastapi import HTTPException
from pytest import raises


from constants.classes import (
    ERROR_CLASSES_INVALID_FIELD_CLASS_EVENTS,
    ERROR_CLASSES_INVALID_FIELD_DAY_OF_WEEK,
    ERROR_CLASSES_INVALID_FIELD_EDUCATION_LEVEL,
    ERROR_CLASSES_INVALID_FIELD_END_DATE,
    ERROR_CLASSES_INVALID_FIELD_ID,
    ERROR_CLASSES_INVALID_FIELD_MAX_STUDENTS,
    ERROR_CLASSES_INVALID_FIELD_SHIFT,
    ERROR_CLASSES_INVALID_FIELD_START_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID,
    ERROR_CLASSES_REQUIRED_FIELD_DAY_OF_WEEK,
    ERROR_CLASSES_REQUIRED_FIELD_DISCIPLINES_ID,
    ERROR_CLASSES_REQUIRED_FIELD_EDUCATION_LEVEL,
    ERROR_CLASSES_REQUIRED_FIELD_END_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_ID,
    ERROR_CLASSES_REQUIRED_FIELD_MAX_STUDENTS,
    ERROR_CLASSES_REQUIRED_FIELD_NAME,
    ERROR_CLASSES_REQUIRED_FIELD_SHIFT,
    ERROR_CLASSES_REQUIRED_FIELD_RECURRENCES,
    ERROR_CLASSES_REQUIRED_FIELD_START_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF,
    ERROR_CLASSES_REQUIRED_FIELD_TEACHER_NAME
)
from constants.disciplines import ERROR_DISCIPLINES_REQUIRED_FIELD_NAME
from schemas.classes import(
    ClassEventRequest,
    ClassEventResponse,
    ClassRequest,
    ClassResponse,
    Recurrences
)


def test_schemas_classes_ClassRequest_success(mock_class_data):

    data = mock_class_data.copy()

    request = ClassRequest(**data)

    assert request.education_level == data['education_level']
    assert request.name == data['name']
    assert request.section == data['section']
    assert request.shift == data['shift']
    assert request.max_students == data['max_students']

    assert isinstance(request.education_level, str)
    assert isinstance(request.shift, str)


def test_schemas_classes_ClassRequest_fail_no_education_level(mock_class_data):

    data = mock_class_data.copy()
    data['education_level'] = " "

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_EDUCATION_LEVEL


def test_schemas_classes_ClassRequest_fail_invalid_education_level(mock_class_data):

    data = mock_class_data.copy()
    data['education_level'] = "hello-world!"

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_EDUCATION_LEVEL


def test_schemas_classes_ClassRequest_fail_no_name(mock_class_data):

    data = mock_class_data.copy()
    data['name'] = " "

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_NAME


def test_schemas_classes_ClassRequest_fail_no_id(mock_class_data):

    data = mock_class_data.copy()
    data['section'] = " "

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_ID


def test_schemas_classes_ClassRequest_fail_invalid_id(mock_class_data):

    data = mock_class_data.copy()
    data['section'] = "hello world!"

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_ID


def test_schemas_classes_ClassRequest_fail_no_shift(mock_class_data):

    data = mock_class_data.copy()
    data['shift'] = " "

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_SHIFT


def test_schemas_classes_ClassRequest_fail_invalid_shift(mock_class_data):

    data = mock_class_data.copy()
    data['shift'] = "hello world!"

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_SHIFT


def test_schemas_classes_ClassRequest_fail_no_max_students(mock_class_data):

    data = mock_class_data.copy()
    data['max_students'] = 0

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_MAX_STUDENTS


def test_schemas_classes_ClassRequest_fail_invalid_max_students_type(mock_class_data):

    data = mock_class_data.copy()
    data['max_students'] =  15.2

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_MAX_STUDENTS


def test_schemas_classes_ClassRequest_fail_invalid_max_students_value(mock_class_data):

    data = mock_class_data.copy()
    data['max_students'] = -1

    with raises(HTTPException) as exception:
        ClassRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_MAX_STUDENTS


def test_schemas_classes_Recurrences_success(mock_recurrences_data):

    data = mock_recurrences_data.copy()

    request = Recurrences(**data)

    assert request.day_of_week == data['day_of_week']
    assert request.start_time == data['start_time']
    assert request.end_time == data['end_time']

    assert isinstance(request.day_of_week, str)
    assert isinstance(request.start_time, str)
    assert isinstance(request.end_time, str)


def test_schemas_classes_Recurrences_fail_no_day_of_week(mock_recurrences_data):
    
        data = mock_recurrences_data.copy()
        data['day_of_week'] = " "
    
        with raises(HTTPException) as exception:
            Recurrences(**data)
    
        assert exception.value.status_code == 422
        assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_DAY_OF_WEEK


def test_schemas_classes_Recurrences_fail_invalid_day_of_week(mock_recurrences_data):

    data = mock_recurrences_data.copy()
    data['day_of_week'] = "hello world!"

    with raises(HTTPException) as exception:
        Recurrences(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_DAY_OF_WEEK


def test_schemas_classes_Recurrences_fail_no_start_time(mock_recurrences_data):
        
            data = mock_recurrences_data.copy()
            data['start_time'] = " "
        
            with raises(HTTPException) as exception:
                Recurrences(**data)
        
            assert exception.value.status_code == 422
            assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_START_DATE


def test_schemas_classes_Recurrences_fail_invalid_start_time(mock_recurrences_data):
         
        data = mock_recurrences_data.copy()
        data['start_time'] = "8:30"
    
        with raises(HTTPException) as exception:
            Recurrences(**data)
    
        assert exception.value.status_code == 422
        assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_START_DATE


def test_schemas_classes_Recurrences_fail_no_end_time(mock_recurrences_data):
    
        data = mock_recurrences_data.copy()
        data['end_time'] = " "
    
        with raises(HTTPException) as exception:
            Recurrences(**data)
    
        assert exception.value.status_code == 422
        assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_END_DATE


def test_schemas_classes_Recurrences_fail_invalid_end_time(mock_recurrences_data):
        
            data = mock_recurrences_data.copy()
            data['end_time'] = "9:30"
        
            with raises(HTTPException) as exception:
                Recurrences(**data)
        
            assert exception.value.status_code == 422
            assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_END_DATE


def test_schemas_classes_ClassEventRequest_success(mock_class_event_request_data):
     
    data = mock_class_event_request_data.copy()

    request = ClassEventRequest(**data)

    assert request.class_id == data['class_id']
    assert request.disciplines_id == data['disciplines_id']
    assert isinstance(request.disciplines_id, list)
    assert isinstance(request.disciplines_id[0], str)
    assert request.disciplines_id[0] == data["disciplines_id"][0]
    assert request.teacher_id == data['teacher_id']
    assert request.start_date == data['start_date']
    assert request.end_date == data['end_date']
    assert request.recurrences == [
         Recurrences(
            day_of_week=recurrence_date["day_of_week"],
            start_time = recurrence_date["start_time"],
            end_time= recurrence_date["end_time"]
            ) for recurrence_date in data['recurrences']]


def test_schemas_classes_ClassEventRequest_fail_no_class_id(mock_class_event_request_data):
        
    data = mock_class_event_request_data.copy()
    data['class_id'] = " "

    with raises(HTTPException) as exception:
        ClassEventRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID


def test_schemas_classes_ClassEventRequest_fail_no_disciplines_id(mock_class_event_request_data):
     
    data = mock_class_event_request_data.copy()
    data['disciplines_id'] = " "

    with raises(HTTPException) as exception:
        ClassEventRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_DISCIPLINES_ID


def test_schemas_classes_ClassEventRequest_fail_no_teacher_id(mock_class_event_request_data):
     
    data = mock_class_event_request_data.copy()
    data['teacher_id'] = " "

    with raises(HTTPException) as exception:
        ClassEventRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF


def test_schemas_classes_ClassEventRequest_fail_no_start_date(mock_class_event_request_data):
     
    data = mock_class_event_request_data.copy()
    data['start_date'] = " "

    with raises(HTTPException) as exception:
        ClassEventRequest(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_START_DATE


def test_schemas_classes_ClassEventRequest_fail_no_end_date(mock_class_event_request_data):
         
        data = mock_class_event_request_data.copy()
        data['end_date'] = " "
    
        with raises(HTTPException) as exception:
            ClassEventRequest(**data)
    
        assert exception.value.status_code == 422
        assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_END_DATE


def test_schemas_classes_ClassEventRequest_fail_no_recurrences(mock_class_event_request_data):
         
        data = mock_class_event_request_data.copy()
        data['recurrences'] = {}
    
        with raises(HTTPException) as exception:
            ClassEventRequest(**data)
    
        assert exception.value.status_code == 422
        assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_RECURRENCES


def test_schemas_classes_ClassEventResponse_success(mock_class_event_response_data):
     
    data = mock_class_event_response_data.copy()

    response = ClassEventResponse(**data)

    assert response.id == data["id"]
    assert response.class_id == data['class_id']
    assert response.disciplines_id == data['disciplines_id']
    assert response.teacher_id == data['teacher_id']
    assert response.start_date == data['start_date']
    assert response.end_date == data['end_date']
    assert response.recurrences == [
        Recurrences(
            day_of_week=recurrence_date["day_of_week"],
            start_time = recurrence_date["start_time"],
            end_time= recurrence_date["end_time"]
        ) for recurrence_date in data['recurrences']
    ]
    assert response.teacher_name == data['teacher_name']
    assert response.discipline_name == data['discipline_name']


def test_schemas_classes_ClassEventResponse_fail_no_teacher_name(mock_class_event_response_data):
     
    data = mock_class_event_response_data.copy()
    data['teacher_name'] = " "

    with raises(HTTPException) as exception:
        ClassEventResponse(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_TEACHER_NAME


def test_schemas_classes_ClassEventResponse_fail_no_discipline_name(mock_class_event_response_data):
     
    data = mock_class_event_response_data.copy()
    data['discipline_name'] = " "

    with raises(HTTPException) as exception:
        ClassEventResponse(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_DISCIPLINES_REQUIRED_FIELD_NAME


def test_schemas_classes_ClassResponse_success(mock_class_response_data):

    data = mock_class_response_data.copy()
    data["id"] = "capeta"
    response = ClassResponse(**data)

    assert response.id == data["id"]
    assert response.education_level == data['education_level']
    assert response.name == data['name']
    assert response.section == data['section']
    assert response.shift == data['shift']
    assert response.max_students == data['max_students']
    assert response.class_info == data['class_info']
    assert response.class_events == [
        ClassEventResponse(**response) for response in data['class_events']
    ]


def test_schemas_classes_ClassResponse_fail_no_class_info   (mock_class_response_data):
     
    data = mock_class_response_data.copy()
    data['class_info'] = " "

    with raises(HTTPException) as exception:
        ClassResponse(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_REQUIRED_FIELD_NAME



def test_schemas_classes_ClassResponse_fail_no_class_events_invalid_class_events(mock_class_response_data):
     
    data = mock_class_response_data.copy()
    data['class_events'] = {}

    with raises(HTTPException) as exception:
        ClassResponse(**data)

    assert exception.value.status_code == 422
    assert exception.value.detail == ERROR_CLASSES_INVALID_FIELD_CLASS_EVENTS


def test_schemas_classes_ClassResponse_success_no_class_events_no_class_events(mock_class_response_data):
     
    data = mock_class_response_data.copy()
    data['class_events'] = []
    data["id"] = "capeta"

    response = ClassResponse(**data)

    assert response.class_events == []