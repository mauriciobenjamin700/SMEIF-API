from fastapi import HTTPException
from pytest import raises


from constants.disciplines import ERROR_DISCIPLINES_GET_NOT_FOUND
from useCases.disciplines import DisciplinesUseCases
from schemas.disciplines import DisciplineResponse


def test_uc_disciplines_get_success(db_session, mock_discipline_on_db):


    uc = DisciplinesUseCases(db_session)
    discipline = uc.get(mock_discipline_on_db.name)

    assert isinstance(discipline, DisciplineResponse)
    assert discipline.id == mock_discipline_on_db.id
    assert discipline.name == mock_discipline_on_db.name
    

def test_uc_disciplines_get_fail(db_session, mock_discipline_on_db):

    uc = DisciplinesUseCases(db_session)

    with raises(HTTPException) as exception:
        uc.get("Disciplina não existente")

    assert exception.value.status_code == 404
    assert exception.value.detail == ERROR_DISCIPLINES_GET_NOT_FOUND