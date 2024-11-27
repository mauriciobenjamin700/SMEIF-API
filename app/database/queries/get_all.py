from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session


from constants.user import ERROR_USER_NOT_FOUND_USERS
from database.models import(
    ClassEventModel,
    ClassModel,
    UserModel
)
from utils.messages.error import NotFound
from constants.classes import (
    ERROR_CLASSES_GET_ALL_NOT_FOUND,
)


def get_all_users(db_session: Session) -> list[UserModel]:
    """
    Busca todos os usuários no banco de dados

    - Args:
        - db_session: Sessão do banco de dados

    - Returns:
        - list[UserModel]: Lista de usuários encontrados no banco de dados.
    """
    users = db_session.scalars(select(UserModel)).all()

    if not users:
        raise NotFound(ERROR_USER_NOT_FOUND_USERS)
    
    return users


def get_all_classes(db_session: Session) -> list[ClassModel]:
    """
    Busca todas as turmas no banco de dados

    - Args:
        - db_session: Sessão do banco de dados

    - Returns:
        - list[ClassModel]: Lista de turmas encontradas no banco de dados.
    """
    classes =  db_session.scalars(
        select(ClassModel)
    ).all()
    if not classes:
        raise NotFound(ERROR_CLASSES_GET_ALL_NOT_FOUND)
    

    return classes

def get_all_class_events_from_class(db_session: Session, class_id: str) -> list[ClassEventModel]:
    """
    Busca todos as aulas de uma determinada turma

    - Args:
        - db_session: Sessão do banco de dados

    - Returns:
        - list[str]: Lista de eventos das turmas encontradas no banco de dados.
    """
    events = db_session.scalars(
        select(ClassEventModel).where(ClassEventModel.class_id == class_id)
    ).all()

    return events


def get_all_class_events(db_session: Session) -> Sequence[ClassEventModel]:
    """
    Busca todos os eventos de todas as turmas

    - Args:
        - db_session: Sessão do banco de dados

    - Returns:
        - list[str]: Lista de eventos das turmas encontradas no banco de dados.
    """
    events = db_session.scalars(select(ClassEventModel)).all()

    return events
