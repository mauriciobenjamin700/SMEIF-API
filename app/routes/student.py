from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session


from useCases.student import StudentUseCases
from routes.docs.student import (
    ADD_DESCRIPTION,
    GET_DESCRIPTION,
    LIST_DESCRIPTION,
    UPDATE_DESCRIPTION,
    DELETE_DESCRIPTION,
    CHANGE_CLASS_DESCRIPTION,
    ADD_PARENT_DESCRIPTION,
    REMOVE_PARENT_DESCRIPTION,
    ADD_RESPONSES,
    GET_RESPONSES,
    LIST_RESPONSES,
    UPDATE_RESPONSES,
    DELETE_RESPONSES,
    CHANGE_CLASS_RESPONSES,
    ADD_PARENT_RESPONSES,
    REMOVE_PARENT_RESPONSES 
)
from schemas.base import (
    BaseMessage,
    Kinship
)
from schemas.child import(
    ChildRequest,
    StudentRequest,
    StudentResponse
)
from services.session import db_session


router = APIRouter(prefix="/student", tags=["student"])


@router.post("/add", status_code=201, description=ADD_DESCRIPTION, responses=ADD_RESPONSES)
async def add_student(
    request: StudentRequest,
    db_session: Session = Depends(db_session)
) -> StudentResponse:
    
    uc = StudentUseCases(db_session)
    
    response = uc.add(request)
    
    return response


@router.get("/get", description=GET_DESCRIPTION, responses=GET_RESPONSES)
def get_student(
    student_cpf: str,
    db_session: Session = Depends(db_session)
) -> StudentResponse:
    
    uc = StudentUseCases(db_session)
    
    response = uc.get(student_cpf)
    
    return response


@router.get("/list", description=LIST_DESCRIPTION, responses=LIST_RESPONSES)
def list_students(
    db_session: Session = Depends(db_session)
) -> list[StudentResponse]:
    
    uc = StudentUseCases(db_session)
    
    response = uc.get_all()
    
    return response


@router.put("/update", description=UPDATE_DESCRIPTION, responses=UPDATE_RESPONSES)
async def update_student(
    request: ChildRequest,
    db_session: Session = Depends(db_session)
) -> StudentResponse:
    
    uc = StudentUseCases(db_session)
    
    response = uc.update(request)
    
    return response


@router.delete("/delete", description=DELETE_DESCRIPTION, responses=DELETE_RESPONSES)
def delete_student(
    student_cpf: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
    
    uc = StudentUseCases(db_session)
    
    response = uc.delete(student_cpf)
    
    return response


@router.put("/change-class", description=CHANGE_CLASS_DESCRIPTION, responses=CHANGE_CLASS_RESPONSES)
def change_student_class(
    student_cpf: str,
    to_class_id: str,
    is_transfer: bool = True,
    db_session: Session = Depends(db_session)
) -> StudentResponse:
    
    uc = StudentUseCases(db_session)
    
    response = uc.change_class(student_cpf, to_class_id, is_transfer)
    
    return response


@router.put("/add-parent", description=ADD_PARENT_DESCRIPTION, responses=ADD_PARENT_RESPONSES)
def add_student_parent(
    student_cpf: str,
    kinship: Kinship,
    parent_cpf: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
    
    uc = StudentUseCases(db_session)
    
    response = uc.add_parent(student_cpf, kinship, parent_cpf)
    
    return response


@router.put("/remove-parent", description=REMOVE_PARENT_DESCRIPTION, responses=REMOVE_PARENT_RESPONSES)
def remove_student_parent(
    student_cpf: str,
    parent_cpf: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
    
    uc = StudentUseCases(db_session)
    
    response = uc.delete_parent(student_cpf, parent_cpf)
    
    return response