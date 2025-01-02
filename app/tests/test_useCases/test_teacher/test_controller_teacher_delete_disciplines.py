from database.models import TeacherDisciplinesModel
from useCases.teacher import TeacherUseCases
from schemas.teacher import TeacherDisciplinesRequest


def test_uc_teacher_delete_discipline_success(
    db_session,
    mock_teacher_on_db,
    mock_teacher_discipline_on_db
):
    
    uc = TeacherUseCases(db_session)

    request = TeacherDisciplinesRequest(
        user_cpf=mock_teacher_discipline_on_db.user_cpf,
        disciplines_id=[mock_teacher_discipline_on_db.discipline_id]
    )

    discipline = db_session.query(TeacherDisciplinesModel).filter(
        TeacherDisciplinesModel.user_cpf == request.user_cpf,
        TeacherDisciplinesModel.discipline_id == request.disciplines_id[0]
    ).first()

    assert discipline is not None
    
    response = uc.delete_disciplines(request)

    assert response.disciplines == []


