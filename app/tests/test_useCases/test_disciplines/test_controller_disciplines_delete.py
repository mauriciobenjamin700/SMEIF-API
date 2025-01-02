from constants.disciplines import MESSAGE_DISCIPLINE_DELETE_SUCCESS
from useCases.disciplines import DisciplinesUseCases
from database.models import DisciplinesModel


def test_uc_disciplines_delete(db_session, mock_discipline_on_db):

    uc = DisciplinesUseCases(db_session)

    response = uc.delete(mock_discipline_on_db.name)

    assert response.detail == MESSAGE_DISCIPLINE_DELETE_SUCCESS

    assert db_session.query(DisciplinesModel).filter(
        DisciplinesModel.name == mock_discipline_on_db.name
    ).first() is None