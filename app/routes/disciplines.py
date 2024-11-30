from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session


from controllers.disciplines import DisciplinesController
from schemas.disciplines import(
    DisciplineRequest,
    DisciplineResponse
)
from schemas.base import BaseMessage
from services.session import db_session


router = APIRouter(prefix='/disciplines', tags=['Disciplines'])


@router.post('/add')
async def add_discipline(
    request: DisciplineRequest,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
    
    uc = DisciplinesController(db_session)

    response = uc.add(request)

    return response


@router.get("/get")
async def get_discipline(
    discipline_name: str,
    db_session: Session = Depends(db_session)
) -> DisciplineResponse:

    uc = DisciplinesController(db_session)

    response = uc.get(discipline_name)

    return response


@router.get("/list")
async def list_disciplines(
    db_session: Session = Depends(db_session)
) -> list[DisciplineResponse]:

    uc = DisciplinesController(db_session)

    response = uc.get_all()

    return response


@router.put("/update")
async def update_discipline(
    name:str,
    request: DisciplineRequest,
    db_session: Session = Depends(db_session)
) -> DisciplineResponse:
    
        uc = DisciplinesController(db_session)
    
        response = uc.update(name, request)
    
        return response


@router.delete("/delete")
async def delete_discipline(
    discipline_name: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = DisciplinesController(db_session)

    response = uc.delete(discipline_name)

    return response