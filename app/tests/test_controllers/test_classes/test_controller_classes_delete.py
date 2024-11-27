from constants.classes import MESSAGE_CLASS_DELETE_SUCCESS
from controllers.classes import ClassesController


def test_controller_classes_delete(db_session, mock_class_on_db):

    uc = ClassesController(db_session)

    response = uc.delete(mock_class_on_db.id)

    assert response.detail == MESSAGE_CLASS_DELETE_SUCCESS