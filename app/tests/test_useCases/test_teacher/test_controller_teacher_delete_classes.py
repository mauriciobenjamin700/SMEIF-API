from useCases.teacher import TeacherUseCases
from schemas.teacher import ClassTeacherRequest


def test_uc_teacher_delete_classes_success(
    db_session,
    mock_class_teacher_on_db
):
    
    uc = TeacherUseCases(db_session)

    request = ClassTeacherRequest(
        user_cpf=mock_class_teacher_on_db.user_cpf,
        classes_id=[mock_class_teacher_on_db.class_id]
    )
    
    response = uc.delete_classes(request)

    assert response.classes == []


