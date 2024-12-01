from controllers.teacher import TeacherController
from schemas.teacher import ClassTeacherRequest

def test_controller_teacher_add_classes_success_one(
    db_session,
    mock_teacher_on_db,
    mock_ClassTeacherRequest
):
    
    controller = TeacherController(db_session)

    request = ClassTeacherRequest(**mock_ClassTeacherRequest.dict())

    response = controller.add_classes(request)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == mock_teacher_on_db.cpf
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == mock_teacher_on_db.phone

    assert response.classes[0].id == request.classes_id[0]