from sqlalchemy import select
from sqlalchemy.orm import Session


from constants.classes import(
    ERROR_CLASSES_EVENTS_GET_NOT_FOUND,
    ERROR_CLASSES_GET_NOT_FOUND
)
from constants.disciplines import ERROR_DISCIPLINES_GET_NOT_FOUND
from constants.user import (
    ERROR_USER_GET_TEACHER_NOT_FOUND,
    ERROR_USER_NOT_ID,
    ERROR_USER_REQUIRED_FIELD_CPF,
    ERROR_USER_NOT_FOUND_USER
)
from database.models import(
    ClassEventModel,
    ClassModel,
    DisciplinesModel,
    UserModel
)
from schemas.base import UserLevel
from utils.messages.error import (
    BadRequest, 
    NotFound
)


def get_user_by_cpf(db_session: Session, cpf:str) -> UserModel:

    if not cpf:
        raise BadRequest(ERROR_USER_REQUIRED_FIELD_CPF)

    model = db_session.scalar(
        select(UserModel).where(
            UserModel.cpf == cpf
            )
    )

    if not model:
        raise NotFound(ERROR_USER_NOT_FOUND_USER)
    
    return model


def get_teacher_by_cpf(db_session: Session, teacher_cpf:str) -> UserModel:

    model = db_session.scalar(
        select(UserModel).where(
            UserModel.cpf == teacher_cpf & 
            UserModel.level == UserLevel.TEACHER.value
        )
    )

    if not model:
        raise NotFound(ERROR_USER_GET_TEACHER_NOT_FOUND)
    
    return model


def get_class_by_id(db_session: Session, class_id:str) -> ClassModel:

    model = db_session.scalar(
        select(ClassModel).where(
            ClassModel.id == class_id
        )
    )

    if not model:
        raise NotFound(ERROR_CLASSES_GET_NOT_FOUND)
    
    return model


def get_class_by_name(db_session: Session, class_name:str) -> ClassModel:

    model = db_session.scalar(
        select(ClassModel).where(
            ClassModel.name == class_name
        )
    )

    if not model:
        raise NotFound(ERROR_CLASSES_GET_NOT_FOUND)
    
    return model


def get_class_event_by_id(db_session: Session, class_event_id:str) -> ClassEventModel:

    model = db_session.scalar(
        select(ClassEventModel).where(
            ClassEventModel.id == class_event_id
        )
    )

    if not model:
        raise NotFound(ERROR_CLASSES_EVENTS_GET_NOT_FOUND)
    
    return model


def get_discipline_by_name(db_session: Session, discipline_name:str) -> DisciplinesModel:

    model = db_session.scalar(
        select(DisciplinesModel).where(
            DisciplinesModel.name == discipline_name
        )
    )

    if not model:
        raise NotFound(ERROR_DISCIPLINES_GET_NOT_FOUND)
    
    return model