from useCases.disciplines import DisciplinesUseCases
from schemas.disciplines import (
    DisciplineRequest,
    DisciplineResponse,
)


def test_uc_disciplines_update_success(db_session, mock_discipline_on_db):
    uc = DisciplinesUseCases(db_session)

    request = DisciplineRequest(
        name="Matemática update"
    )


    response = uc.update(mock_discipline_on_db.name,request)

    assert isinstance(response, DisciplineResponse)
    assert response.name == request.name
    assert response.id == mock_discipline_on_db.id