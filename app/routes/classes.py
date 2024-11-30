from fastapi import (
    APIRouter, 
    Depends
)
from sqlalchemy.orm import Session


from controllers.classes import ClassesController
from schemas.base import BaseMessage
from schemas.classes import(
    ClassEventRequest,
    ClassEventResponse,
    ClassRequest,
    ClassResponse,
    Recurrences,
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
) -> list[ClassResponse]:

    uc = ClassesController(db_session)

    response = uc.get_all()

    return response


@router.put("/update")
async def update_class(
    class_id: str,
    update: ClassRequest,
    db_session: Session = Depends(db_session)
) -> ClassResponse:

    uc = ClassesController(db_session)

    response = uc.update(class_id, update)

    return response


@router.delete("/delete")
async def delete_class(
    class_id: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = ClassesController(db_session)

    response = uc.delete(class_id)

    return response


@router.post("/add-event")
def add_event(
    request: ClassEventRequest,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = ClassesController(db_session)

    response = uc.add_event(request)

    return response


@router.get("/get-event")
async def get_event(
    class_event_id: str,
    db_session: Session = Depends(db_session)
) -> ClassEventResponse:
    
    uc = ClassesController(db_session)

    response = uc.get_event(class_event_id)

    return response


@router.get("/list-events")
async def list_events(
    db_session: Session = Depends(db_session)
) -> list[ClassEventResponse]:
    
        uc = ClassesController(db_session)
    
        response = uc.get_all_events()
    
        return response


@router.put("/update-event")
async def update_event(
    class_event_id: str,
    update: ClassEventRequest,
    db_session: Session = Depends(db_session)
) -> ClassEventResponse:
        
        uc = ClassesController(db_session)
        
        response = uc.update_event(class_event_id, update)
        
        return response


@router.delete("/delete-event")
async def delete_event(
    class_event_id: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
        
        uc = ClassesController(db_session)
        
        response = uc.delete_event(class_event_id)
        
        return response


@router.get("/add-recurrences")
async def add_recurrences(
    class_event_id: str,
    recurrences: list[Recurrences],
    db_session: Session = Depends(db_session)
) -> BaseMessage:
        
        uc = ClassesController(db_session)
        
        response = uc.add_recurrences(class_event_id, recurrences)
        
        return response


@router.put("/delete-recurrences")
async def delete_recurrences(
    class_event_id: str,
    recurrences: list[Recurrences],
    db_session: Session = Depends(db_session)
) -> BaseMessage:
        
        uc = ClassesController(db_session)
        
        response = uc.delete_recurrences(class_event_id, recurrences)
        
        return response