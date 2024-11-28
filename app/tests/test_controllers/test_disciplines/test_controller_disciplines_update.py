from controllers.disciplines import DisciplinesController
from schemas.disciplines import (
    DisciplineRequest,
    DisciplineResponse,
)


def test_controller_disciplines_update_success(db_session, mock_discipline_on_db):
    controller = DisciplinesController(db_session)

    request = DisciplineRequest(
        name="Matemática update"
    )


    response = controller.update(mock_discipline_on_db.name,request)

    assert isinstance(response, DisciplineResponse)
    assert response.name == request.name
    assert response.id == mock_discipline_on_db.id