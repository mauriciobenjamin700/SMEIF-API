from fastapi import HTTPException
from pytest import raises


from constants.disciplines import ERROR_DISCIPLINES_GET_ALL_NOT_FOUND
from constants.teacher import ERROR_TEACHER_ADD_CLASSES_CONFLICT
from constants.user import ERROR_USER_GET_TEACHER_NOT_FOUND

from useCases.teacher import TeacherUseCases
from schemas.teacher import ClassTeacherRequest
from utils.format import (
    format_cpf, 
    format_phone
)


def test_uc_teacher_add_classes_success_one(
    db_session,
    mock_teacher_on_db,
    mock_ClassTeacherRequest
):
    
    uc = TeacherUseCases(db_session)

    request = ClassTeacherRequest(**mock_ClassTeacherRequest.dict())

    response = uc.add_classes(request)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf) 
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone) 

    assert response.classes[0].id == request.classes_id[0]


def test_uc_teacher_add_classes_success_three(
    db_session,
    mock_teacher_on_db,
    mock_list_class_on_db
):
    
    uc = TeacherUseCases(db_session)

    request = ClassTeacherRequest(
        user_cpf=mock_teacher_on_db.cpf,
        classes_id=[class_.id for class_ in mock_list_class_on_db]
    )

    response = uc.add_classes(request)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf)
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone) 


def test_uc_teacher_add_classes_invalid_teacher(
    db_session,
    mock_user_on_db,
    mock_ClassTeacherRequest
):
    
    uc = TeacherUseCases(db_session)

    request = ClassTeacherRequest(
        user_cpf=mock_user_on_db.cpf,
        classes_id=mock_ClassTeacherRequest.classes_id
    )

    with raises(HTTPException) as e:
        uc.add_classes(request)

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_USER_GET_TEACHER_NOT_FOUND


def test_uc_teacher_add_classes_invalid_classes(
    db_session,
    mock_teacher_on_db,
    mock_teacher_discipline_on_db,
    mock_ClassTeacherRequest
):
        
        uc = TeacherUseCases(db_session)
    
        request = ClassTeacherRequest(
            **mock_ClassTeacherRequest.dict()
        )
    
        with raises(HTTPException) as e:
            uc.add_classes(request)
            uc.add_classes(request)
    
        assert e.value.status_code == 409
        assert e.value.detail == ERROR_TEACHER_ADD_CLASSES_CONFLICT
