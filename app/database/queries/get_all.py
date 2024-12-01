from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session


from constants.teacher import ERROR_TEACHER_GET_ALL_NOT_FOUND
from constants.disciplines import ERROR_DISCIPLINES_GET_ALL_NOT_FOUND
from constants.user import ERROR_USER_NOT_FOUND_USERS
from database.models import(
    ClassEventModel,
    ClassModel,
    ClassTeacherModel,
    DisciplinesModel,
    TeacherDisciplinesModel,
    UserModel
)
from schemas.base import UserLevel
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


def get_all_disciplines(db_session: Session) -> list[DisciplinesModel]:
    """
    Busca todas as disciplinas no banco de dados

    - Args:
        - db_session: Sessão do banco de dados

    - Returns:
        - list[str]: Lista de disciplinas encontradas no banco de dados.
    """
    disciplines = db_session.scalars(select(DisciplinesModel)).all()

    if not disciplines:
        raise NotFound(ERROR_DISCIPLINES_GET_ALL_NOT_FOUND)

    return disciplines


def get_all_disciplines_by_teacher(db_session: Session, user_cpf: str) -> list[DisciplinesModel]:
    """
    Busca todas as disciplinas de um professor

    - Args:
        - db_session: Sessão do banco de dados
        - user_cpf: CPF do professor

    - Returns:
        - list[DisciplinesModel]: Lista de disciplinas encontradas no banco de dados.
    """
    associations = db_session.scalars(
        select(TeacherDisciplinesModel).where(TeacherDisciplinesModel.user_cpf == user_cpf)
    ).all()

    # if not associations: # Existem caos que simplesmente não vai ter mesmo (em cadastro)
    #     raise NotFound(ERROR_DISCIPLINES_GET_ALL_NOT_FOUND)

    return [assossiation.discipline for assossiation in associations]


def get_all_classes_by_teacher(db_session: Session, user_cpf: str) -> list[ClassModel]:
    """
    Busca todas as turmas de um professor

    - Args:
        - db_session: Sessão do banco de dados
        - user_cpf: CPF do professor

    - Returns:
        - list[ClassModel]: Lista de turmas encontradas no banco de dados.
    """
    associations = db_session.scalars(
        select(ClassTeacherModel).where(ClassTeacherModel.user_cpf == user_cpf)
    ).all()

    # if not associations: # existem casos que simplesmente não vai ter mesmo
    #     raise NotFound(ERROR_CLASSES_GET_ALL_NOT_FOUND)

    classes = []

    for association in associations:
        classes += association.classes

    return classes


def get_all_teachers(db_session: Session) -> list[UserModel]:
    """
    Busca todos os professores no banco de dados

    - Args:
        - db_session: Sessão do banco de dados

    - Returns:
        - list[UserModel]: Lista de professores encontrados no banco de dados.
    """
    teachers = db_session.scalars(
        select(UserModel).where(
            UserModel.level == UserLevel.TEACHER.value
        )).all()
    
    if not teachers:
        raise NotFound(ERROR_TEACHER_GET_ALL_NOT_FOUND)

    return teachers


def get_all_class_teacher_models_by_filter(db_session: Session, user_cpf: str, classes_id: list[str]) -> list[ClassTeacherModel]:

    classes = db_session.query(ClassTeacherModel).filter(
    ClassTeacherModel.user_cpf == user_cpf,
    ClassTeacherModel.class_id.in_(classes_id)
    ).all()

    if not classes:
        raise NotFound(ERROR_CLASSES_GET_ALL_NOT_FOUND)
    
    return classes


def get_all_teacher_disciplines_by_filter(db_session: Session, user_cpf: str, disciplines_id: list[str]) -> list[TeacherDisciplinesModel]:

    disciplines = db_session.query(TeacherDisciplinesModel).filter(
    TeacherDisciplinesModel.user_cpf == user_cpf,
    TeacherDisciplinesModel.discipline_id.in_(disciplines_id)
    ).all()

    if not disciplines:
        raise NotFound(ERROR_DISCIPLINES_GET_ALL_NOT_FOUND)
    
    return disciplines