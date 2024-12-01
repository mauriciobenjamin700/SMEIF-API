from controllers.teacher import TeacherController
from schemas.teacher import ClassTeacherRequest
from utils.format import format_cpf, format_phone


def test_controller_teacher_add_classes_success_one(
    db_session,
    mock_teacher_on_db,
    mock_teacher_discipline_on_db,
    mock_ClassTeacherRequest
):
    
    controller = TeacherController(db_session)

    request = ClassTeacherRequest(**mock_ClassTeacherRequest.dict())

    response = controller.add_classes(request)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf) 
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone) 

    assert response.classes[0].id == request.classes_id[0]


def test_controller_teacher_add_classes_success_three(
    db_session,
    mock_teacher_on_db,
    mock_teacher_discipline_on_db,
    mock_list_class_on_db
):
    
    controller = TeacherController(db_session)

    request = ClassTeacherRequest(
        user_cpf=mock_teacher_on_db.cpf,
        classes_id=[class_.id for class_ in mock_list_class_on_db]
    )

    response = controller.add_classes(request)

    assert response.user.name == mock_teacher_on_db.name
    assert response.user.cpf == format_cpf(mock_teacher_on_db.cpf)
    assert response.user.email == mock_teacher_on_db.email
    assert response.user.phone == format_phone(mock_teacher_on_db.phone) 

