from fastapi import HTTPException
from pytest import raises


from constants.disciplines import ERROR_DISCIPLINES_GET_ALL_NOT_FOUND
from controllers.disciplines import DisciplinesController
from schemas.disciplines import DisciplineResponse


def test_controller_disciplines_get_all_success(db_session, mock_discipline_on_db):

    uc = DisciplinesController(db_session)
    disciplines = uc.get_all()

    assert isinstance(disciplines, list)
    assert len(disciplines) == 1
    assert isinstance(disciplines[0], DisciplineResponse)
    assert disciplines[0].id == mock_discipline_on_db.id
    assert disciplines[0].name == mock_discipline_on_db.name


def test_controller_disciplines_get_all_fail(db_session):
    
        uc = DisciplinesController(db_session)
    
        with raises(HTTPException) as exception:
            uc.get_all()
    
        assert exception.value.status_code == 404
        assert exception.value.detail == ERROR_DISCIPLINES_GET_ALL_NOT_FOUND