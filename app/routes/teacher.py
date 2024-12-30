from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session


from useCases.teacher import TeacherUseCases
from routes.docs.teacher import (
    ADD_DISCIPLINES_DESCRIPTION,
    ADD_CLASS_RESPONSES,
    ADD_CLASS_DESCRIPTION,
    ADD_DISCIPLINES_RESPONSES,
    GET_TEACHER_DESCRIPTION,
    GET_TEACHER_RESPONSES,
    DELETE_CLASS_DESCRIPTION,
    DELETE_CLASS_RESPONSES,
    DELETE_DISCIPLINES_DESCRIPTION,
    DELETE_DISCIPLINES_RESPONSES,
    LIST_TEACHER_DESCRIPTION,
    LIST_TEACHER_RESPONSES
)
from schemas.teacher import (
    ClassTeacherRequest,
    TeacherDisciplinesRequest,
    TeacherResponse
)
from services.session import db_session


router = APIRouter(prefix='/teacher', tags=['Teacher'])


@router.post('/add-classes', status_code=201, responses=ADD_CLASS_RESPONSES, description=ADD_CLASS_DESCRIPTION)
async def add_class(
    request: ClassTeacherRequest,
    db_session: Session = Depends(db_session)
) -> TeacherResponse:

    uc = TeacherUseCases(db_session)

    response = uc.add_classes(request)

    return response


@router.post('/add-disciplines', status_code=201, responses=ADD_DISCIPLINES_RESPONSES, description=ADD_DISCIPLINES_DESCRIPTION)
async def add_disciplines(
    request: TeacherDisciplinesRequest,
    db_session: Session = Depends(db_session)
) -> TeacherResponse:

    uc = TeacherUseCases(db_session)

    response = uc.add_disciplines(request)

    return response


@router.get('/get', response_model=list[TeacherResponse], description=GET_TEACHER_DESCRIPTION, responses=GET_TEACHER_RESPONSES)
async def get_teacher(
    user_cpf: str,
    db_session: Session = Depends(db_session)
) -> TeacherResponse:

    uc = TeacherUseCases(db_session)

    response = uc.get(user_cpf)

    return response


@router.get('/list', response_model=list[TeacherResponse], description=LIST_TEACHER_DESCRIPTION, responses=LIST_TEACHER_RESPONSES)
async def list_teachers(
    db_session: Session = Depends(db_session)
) -> list[TeacherResponse]:

    uc = TeacherUseCases(db_session)

    response = uc.get_all()

    return response


@router.put('/delete-classes', description=DELETE_CLASS_DESCRIPTION, responses=DELETE_CLASS_RESPONSES)
def delete_classes(
    request: ClassTeacherRequest,
    db_session: Session = Depends(db_session)
) -> TeacherResponse:

    uc = TeacherUseCases(db_session)

    response = uc.delete_classes(request)

    return response


@router.put('/delete-disciplines', description=DELETE_DISCIPLINES_DESCRIPTION, responses=DELETE_DISCIPLINES_RESPONSES)
def delete_disciplines(
    request: TeacherDisciplinesRequest,
    db_session: Session = Depends(db_session)
) -> TeacherResponse:
    
    uc = TeacherUseCases(db_session)

    response = uc.delete_disciplines(request)

    return response