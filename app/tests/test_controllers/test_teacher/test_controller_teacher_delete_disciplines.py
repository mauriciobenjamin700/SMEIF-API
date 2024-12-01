from database.models import TeacherDisciplinesModel
from controllers.teacher import TeacherController
from schemas.teacher import TeacherDisciplinesRequest


def test_controller_teacher_delete_discipline_success(
    db_session,
    mock_teacher_on_db,
    mock_teacher_discipline_on_db
):
    
    controller = TeacherController(db_session)

    request = TeacherDisciplinesRequest(
        user_cpf=mock_teacher_discipline_on_db.user_cpf,
        disciplines_id=[mock_teacher_discipline_on_db.discipline_id]
    )

    discipline = db_session.query(TeacherDisciplinesModel).filter(
        TeacherDisciplinesModel.user_cpf == request.user_cpf,
        TeacherDisciplinesModel.discipline_id == request.disciplines_id[0]
    ).first()

    assert discipline is not None
    
    response = controller.delete_disciplines(request)

    assert response.disciplines == []


