from sqlalchemy import select
from sqlalchemy.orm import Session


from constants.user import ERROR_USER_NOT_FOUND_USERS
from database.models import(
    ClassModel,
    UserModel
)
from utils.messages.error import NotFound
from constants.classes import (
    ERROR_CLASSES_GET_ALL_NOT_FOUND,
)


def get_all_users(db_session: Session) -> list[UserModel]:
        
    users = db_session.scalars(select(UserModel)).all()

    if not users:
        raise NotFound(ERROR_USER_NOT_FOUND_USERS)
    
    return users


def get_all_classes(db_session: Session) -> list[ClassModel]:
    
    classes =  db_session.scalars(
        select(ClassModel)
    )

    if not classes:
        raise NotFound(ERROR_CLASSES_GET_ALL_NOT_FOUND)