from controllers.teacher import TeacherController
from schemas.teacher import ClassTeacherRequest


def test_controller_teacher_delete_classes_success(
    db_session,
    mock_class_teacher_on_db
):
    
    controller = TeacherController(db_session)

    request = ClassTeacherRequest(
        user_cpf=mock_class_teacher_on_db.user_cpf,
        classes_id=[mock_class_teacher_on_db.class_id]
    )
    
    response = controller.delete_classes(request)

    assert response.classes == []


