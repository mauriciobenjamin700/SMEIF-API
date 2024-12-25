from fastapi import HTTPException
from pytest import raises


from constants.classes import ERROR_CLASSES_GET_ALL_NOT_FOUND
from controllers.classes import ClassesController
from schemas.classes import ClassResponse


def test_controller_classes_get_all_success(db_session,mock_class_on_db):

    uc = ClassesController(db_session)

    response = uc.get_all()

    assert isinstance(response, list)
    response = response[0]
    assert isinstance(response, ClassResponse)
    assert response.id == mock_class_on_db.id
    assert response.education_level == mock_class_on_db.education_level
    assert response.name == mock_class_on_db.name
    assert response.section == mock_class_on_db.section
    assert response.shift == mock_class_on_db.shift
    assert response.max_students == mock_class_on_db.max_students
    assert response.class_info == uc.build_class_info(mock_class_on_db)


def test_controller_classes_get_not_found(db_session):

    uc = ClassesController(db_session)

    with raises(HTTPException) as exception:
        uc.get_all()

    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_CLASSES_GET_ALL_NOT_FOUND