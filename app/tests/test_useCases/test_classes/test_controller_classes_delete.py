from constants.classes import MESSAGE_CLASS_DELETE_SUCCESS
from useCases.classes import ClassesUseCases


def test_uc_classes_delete(db_session, mock_class_on_db):

    uc = ClassesUseCases(db_session)

    response = uc.delete(mock_class_on_db.id)

    assert response.detail == MESSAGE_CLASS_DELETE_SUCCESS