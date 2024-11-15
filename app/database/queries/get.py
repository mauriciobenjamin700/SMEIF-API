from sqlalchemy import select
from sqlalchemy.orm import Session


from constants.classes import(
    ERROR_CLASSES_GET_NOT_FOUND
)
from constants.user import (
    ERROR_USER_GET_TEACHER_NOT_FOUND, 
    LEVEL
)
from database.models import(
    ClassModel,
    UserModel
)
from app.utils.messages.messages import NotFoundErrorMessage


def get_teacher_by_cpf(db_session: Session, teacher_cpf:str) -> UserModel:

    model = db_session.scalar(
        select(UserModel).where(
            UserModel.cpf == teacher_cpf & 
            UserModel.level == LEVEL["teacher"]
        )
    )

    if not model:
        raise NotFoundErrorMessage(ERROR_USER_GET_TEACHER_NOT_FOUND)
    
    return model


def get_class_by_id(db_session: Session, class_id:str) -> ClassModel:

    model = db_session.scalar(
        select(ClassModel).where(
            ClassModel.id == class_id
        )
    )

    if not model:
        raise NotFoundErrorMessage(ERROR_CLASSES_GET_NOT_FOUND)
    
    return model


def get_class_by_name(db_session: Session, class_name:str) -> ClassModel:

    model = db_session.scalar(
        select(ClassModel).where(
            ClassModel.name == class_name
        )
    )

    if not model:
        raise NotFoundErrorMessage(ERROR_CLASSES_GET_NOT_FOUND)
    
    return model