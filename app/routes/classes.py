from fastapi import (
    APIRouter, 
    Depends
)
from sqlalchemy.orm import Session


from useCases.classes import ClassesUseCases
from routes.docs.classes import(
    ADD_DESCRIPTION,
    ADD_RESPONSES,
    DELETE_RESPONSES,
    GET_DESCRIPTION,
    GET_RESPONSES,
    LIST_DESCRIPTION,
    LIST_RESPONSES,
    UPDATE_DESCRIPTION,
    DELETE_DESCRIPTION,
    ADD_EVENT_DESCRIPTION,
    GET_EVENT_DESCRIPTION,
    LIST_EVENTS_DESCRIPTION,
    UPDATE_EVENT_DESCRIPTION,
    DELETE_EVENT_DESCRIPTION,
    ADD_RECURRENCES_DESCRIPTION,
    DELETE_RECURRENCES_DESCRIPTION,
    ADD_EVENT_RESPONSES,
    GET_EVENT_RESPONSES,
    LIST_EVENTS_RESPONSES,
    UPDATE_EVENT_RESPONSES,
    DELETE_EVENT_RESPONSES,
    ADD_RECURRENCES_RESPONSES,
    DELETE_RECURRENCES_RESPONSES,
    UPDATE_RESPONSES,

)
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


@router.post('/add', description=ADD_DESCRIPTION, responses=ADD_RESPONSES, status_code=201)
async def add_class(
    request: ClassRequest,
    db_session: Session = Depends(db_session),
) -> BaseMessage:    

    uc = ClassesUseCases(db_session)

    response = uc.add(request)

    return response


@router.get("/get", description=GET_DESCRIPTION, responses=GET_RESPONSES)
async def get_class(
    class_id: str,
    db_session: Session = Depends(db_session)
) -> ClassResponse:

    uc = ClassesUseCases(db_session)

    response = uc.get(class_id)

    return response


@router.get("/list", description=LIST_DESCRIPTION, responses=LIST_RESPONSES)
async def list_classes(
    db_session: Session = Depends(db_session)
) -> list[ClassResponse]:

    uc = ClassesUseCases(db_session)

    response = uc.get_all()

    return response


@router.put("/update", description=UPDATE_DESCRIPTION, responses=UPDATE_RESPONSES)
async def update_class(
    class_id: str,
    update: ClassRequest,
    db_session: Session = Depends(db_session)
) -> ClassResponse:

    uc = ClassesUseCases(db_session)

    response = uc.update(class_id, update)

    return response


@router.delete("/delete", description=DELETE_DESCRIPTION, responses=DELETE_RESPONSES)
async def delete_class(
    class_id: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = ClassesUseCases(db_session)

    response = uc.delete(class_id)

    return response


@router.post("/add-event", description=ADD_EVENT_DESCRIPTION, responses=ADD_EVENT_RESPONSES, status_code=201)
def add_event(
    request: ClassEventRequest,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = ClassesUseCases(db_session)

    response = uc.add_event(request)

    return response


@router.get("/get-event", description=GET_EVENT_DESCRIPTION, responses=GET_EVENT_RESPONSES)
async def get_event(
    class_event_id: str,
    db_session: Session = Depends(db_session)
) -> ClassEventResponse:
    
    uc = ClassesUseCases(db_session)

    response = uc.get_event(class_event_id)

    return response


@router.get("/list-events", description=LIST_EVENTS_DESCRIPTION, responses=LIST_EVENTS_RESPONSES)
async def list_events(
    db_session: Session = Depends(db_session)
) -> list[ClassEventResponse]:
    
    uc = ClassesUseCases(db_session)

    response = uc.get_all_events()

    return response


@router.put("/update-event", description=UPDATE_EVENT_DESCRIPTION, responses=UPDATE_EVENT_RESPONSES)
async def update_event(
    class_event_id: str,
    update: ClassEventRequest,
    db_session: Session = Depends(db_session)
) -> ClassEventResponse:
        
    uc = ClassesUseCases(db_session)
    
    response = uc.update_event(class_event_id, update)
    
    return response


@router.delete("/delete-event", description=DELETE_EVENT_DESCRIPTION, responses=DELETE_EVENT_RESPONSES)
async def delete_event(
    class_event_id: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
        
    uc = ClassesUseCases(db_session)
    
    response = uc.delete_event(class_event_id)
    
    return response


@router.post("/add-recurrences",description=ADD_RECURRENCES_DESCRIPTION, responses=ADD_RECURRENCES_RESPONSES, status_code=201)
async def add_recurrences(
    class_event_id: str,
    recurrences: list[Recurrences],
    db_session: Session = Depends(db_session)
) -> BaseMessage:
        
    uc = ClassesUseCases(db_session)
    
    response = uc.add_recurrences(class_event_id, recurrences)
    
    return response


@router.put("/delete-recurrences", description=DELETE_RECURRENCES_DESCRIPTION, responses=DELETE_RECURRENCES_RESPONSES)
async def delete_recurrences(
    class_event_id: str,
    recurrences: list[Recurrences],
    db_session: Session = Depends(db_session)
) -> BaseMessage:
        
    uc = ClassesUseCases(db_session)
    
    response = uc.delete_recurrences(class_event_id, recurrences)
    
    return response