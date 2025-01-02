from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session


from routes.docs.note import(
    ADD_DESCRIPTION,
    ADD_RESPONSES,
    DELETE_DESCRIPTION,
    DELETE_RESPONSES,
    LIST_DESCRIPTION,
    LIST_RESPONSES,
    UPDATE_DESCRIPTION,
    UPDATE_RESPONSES
)
from schemas.base import BaseMessage
from schemas.note import(
    NoteFilters,
    NoteRequest,
    NoteResponse,
    NoteUpdate
)
from services.session import db_session
from useCases.note import NoteUseCases


router = APIRouter(prefix='/notes', tags=['Notes'])


@router.post('/add', description=ADD_DESCRIPTION,responses=ADD_RESPONSES, status_code=201)
async def add_note(
    request: NoteRequest,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
    
    uc = NoteUseCases(db_session)

    response = uc.add(request)

    return response


@router.get("/list", description=LIST_DESCRIPTION,responses=LIST_RESPONSES)
async def list_notes(
    class_id: str | None = None,
    discipline_id: str | None = None,
    child_cpf: str | None = None,
    semester: str | None = None,
    aval_number: int | None = None,
    db_session: Session = Depends(db_session)
) -> list[NoteResponse]:

    uc = NoteUseCases(db_session)

    filters: NoteFilters = NoteFilters(
        class_id=class_id,
        discipline_id=discipline_id,
        child_cpf=child_cpf,
        semester=semester,
        aval_number=aval_number
    )

    response = uc.get_all(filters)

    return response


@router.put('/update', description=UPDATE_DESCRIPTION,responses=UPDATE_RESPONSES)
async def update_note(
    request: NoteUpdate,
    db_session: Session = Depends(db_session)
) -> NoteResponse:
    
    uc = NoteUseCases(db_session)

    response = uc.update(request)

    return response


@router.delete('/delete', description=DELETE_DESCRIPTION,responses=DELETE_RESPONSES)
async def delete_note(
    note_id: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
    
    uc = NoteUseCases(db_session)

    response = uc.delete(note_id)

    return response