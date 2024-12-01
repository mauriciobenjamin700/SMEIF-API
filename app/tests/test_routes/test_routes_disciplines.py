from constants.disciplines import (
    MESSAGE_DISCIPLINE_ADD_SUCCESS,
    MESSAGE_DISCIPLINE_DELETE_SUCCESS
)
from schemas.disciplines import DisciplineResponse


def test_route_disciplines_add(api, mock_DisciplineRequest):

    request = mock_DisciplineRequest.dict()

    response = api.post("/disciplines/add", json=request)

    assert response.status_code == 201
    assert response.json() == {"detail": MESSAGE_DISCIPLINE_ADD_SUCCESS}


def test_route_disciplines_get(api, mock_discipline_on_db):

    discipline = mock_discipline_on_db

    response = api.get(f"/disciplines/get?discipline_name={discipline.name}")

    assert response.status_code == 200
    assert response.json() == DisciplineResponse(**mock_discipline_on_db.dict()).dict()


def test_route_disciplines_list(api, mock_discipline_on_db):
    
    response = api.get("/disciplines/list")

    assert response.status_code == 200
    assert response.json() == [DisciplineResponse(**mock_discipline_on_db.dict()).dict()]


def test_route_disciplines_update(api, mock_discipline_on_db, mock_DisciplineRequest):
    
    discipline = mock_discipline_on_db
    request = mock_DisciplineRequest.dict()

    response = api.put(f"/disciplines/update?name={discipline.name}", json=request)

    data = response.json()

    data = DisciplineResponse(**data)

    assert response.status_code == 200
    assert data.id == discipline.id
    assert data.name == request["name"]


def test_route_disciplines_delete(api, mock_discipline_on_db):
    
    discipline = mock_discipline_on_db

    response = api.delete(f"/disciplines/delete?discipline_name={discipline.name}")

    assert response.status_code == 200
    assert response.json() == {"detail": MESSAGE_DISCIPLINE_DELETE_SUCCESS}