from fastapi import HTTPException
from pytest import raises


from constants.teacher import ERROR_TEACHER_ADD_DISCIPLINES_CONFLICT
from controllers.teacher import TeacherController
from schemas.teacher import (
    TeacherDisciplinesRequest, 
    TeacherResponse
)

def test_controller_teacher_add_disciplines_success(
    db_session,
    mock_teacher_on_db,
    mock_mock_TeacherDisciplinesRequest
):
    
    controller = TeacherController(db_session)

    request = TeacherDisciplinesRequest(**mock_mock_TeacherDisciplinesRequest.dict())

    response = controller.add_disciplines(request)

    assert isinstance(response, TeacherResponse)

    assert response.user.name == mock_teacher_on_db.name
    assert response.disciplines[0].id == request.disciplines_id[0]



def test_controller_teacher_add_disciplines_already_add(
    db_session,
    mock_teacher_on_db,
    mock_teacher_discipline_on_db,
):
    
    controller = TeacherController(db_session)

    request = TeacherDisciplinesRequest(
        user_cpf=mock_teacher_on_db.cpf,
        disciplines_id=[mock_teacher_discipline_on_db.discipline_id]
    )

    with raises(HTTPException) as e:

        controller.add_disciplines(request)

    assert e.value.status_code == 409
    assert e.value.detail == ERROR_TEACHER_ADD_DISCIPLINES_CONFLICT