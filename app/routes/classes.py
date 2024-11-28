from fastapi import (
    APIRouter, 
    Depends
)
from sqlalchemy.orm import Session


from controllers.classes import ClassesController
from schemas.base import BaseMessage
from schemas.classes import(
    ClassRequest,
    ClassResponse,
)
from services.session import db_session



router = APIRouter(prefix='/classes', tags=['Classes'])


@router.post('/add')
async def add_class(
    request: ClassRequest,
    db_session: Session = Depends(db_session),
) -> BaseMessage:    

    uc = ClassesController(db_session)

    response = uc.add(request)

    return response


@router.get("/get")
async def get_class(
    class_id: str,
    db_session: Session = Depends(db_session)
) -> ClassResponse:

    uc = ClassesController(db_session)

    response = uc.get(class_id)

    return response


@router.get("/list")
async def list_classes(
    db_session: Session = Depends(db_session)
) -> ClassResponse:

    uc = ClassesController(db_session)

    response = uc.get_all()

    return response


@router.delete("/delete")
async def delete_class(
    class_id: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = ClassesController(db_session)

    response = uc.delete(class_id)

    return response


@router.put("/update")
async def update_class(
    class_id: str,
    update: ClassRequest,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = ClassesController(db_session)

    response = uc.update(class_id, update)

    return response