from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session


from controllers.disciplines import DisciplinesController
from routes.docs.disciplines import(
    ADD_DESCRIPTION,
    GET_DESCRIPTION,
    LIST_DESCRIPTION,
    UPDATE_DESCRIPTION,
    DELETE_DESCRIPTION,
    ADD_RESPONSES,
    GET_RESPONSES,
    LIST_RESPONSES,
    UPDATE_RESPONSES,
    DELETE_RESPONSES
)
from schemas.disciplines import(
    DisciplineRequest,
    DisciplineResponse
)
from schemas.base import BaseMessage
from services.session import db_session


router = APIRouter(prefix='/disciplines', tags=['Disciplines'])


@router.post('/add', description=ADD_DESCRIPTION, responses=ADD_RESPONSES, status_code=201)
async def add_discipline(
    request: DisciplineRequest,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
    
    uc = DisciplinesController(db_session)

    response = uc.add(request)

    return response


@router.get("/get", description=GET_DESCRIPTION, responses=GET_RESPONSES)
async def get_discipline(
    discipline_name: str,
    db_session: Session = Depends(db_session)
) -> DisciplineResponse:

    uc = DisciplinesController(db_session)

    response = uc.get(discipline_name)

    return response


@router.get("/list", description=LIST_DESCRIPTION, responses=LIST_RESPONSES)
async def list_disciplines(
    db_session: Session = Depends(db_session)
) -> list[DisciplineResponse]:

    uc = DisciplinesController(db_session)

    response = uc.get_all()

    return response


@router.put("/update", description=UPDATE_DESCRIPTION, responses=UPDATE_RESPONSES)
async def update_discipline(
    name:str,
    request: DisciplineRequest,
    db_session: Session = Depends(db_session)
) -> DisciplineResponse:
    
        uc = DisciplinesController(db_session)
    
        response = uc.update(name, request)
    
        return response


@router.delete("/delete", description=DELETE_DESCRIPTION, responses=DELETE_RESPONSES)
async def delete_discipline(
    discipline_name: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = DisciplinesController(db_session)

    response = uc.delete(discipline_name)

    return response