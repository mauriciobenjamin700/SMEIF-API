from constants.disciplines import MESSAGE_DISCIPLINE_DELETE_SUCCESS
from controllers.disciplines import DisciplinesController
from database.models import DisciplinesModel


def test_controller_disciplines_delete(db_session, mock_discipline_on_db):

    controller = DisciplinesController(db_session)

    response = controller.delete(mock_discipline_on_db.name)

    assert response.detail == MESSAGE_DISCIPLINE_DELETE_SUCCESS

    assert db_session.query(DisciplinesModel).filter(
        DisciplinesModel.name == mock_discipline_on_db.name
    ).first() is None