from sqlalchemy import (
    and_,
    or_,
    select
)
from sqlalchemy.orm import Session


from constants.user import (
    ERROR_USER_CPF_ALREADY_EXISTS,
    ERROR_USER_EMAIL_ALREADY_EXISTS,
    ERROR_USER_PHONE_ALREADY_EXISTS,
    LEVEL
)
from database.base import BaseModel
from database.models import (
    ClassEventModel,
    UserModel,
    ClassModel
)
from schemas.classes import ClassEventRequest
from utils.format import unformat_date
from utils.messages.error import Conflict


def check_user_existence(db_session: Session, cpf: str | None, phone: str | None, email: str | None) -> None:
    filters = []
    
    if cpf:
        filters.append(UserModel.cpf == cpf)
    if phone:
        filters.append(UserModel.phone == phone)
    if email:
        filters.append(UserModel.email == email)
    
    if filters:
        user = db_session.query(UserModel).filter(or_(*filters)).first()
        
        if user:
            if cpf and user.cpf == cpf:
                raise Conflict(ERROR_USER_CPF_ALREADY_EXISTS)
            if phone and user.phone == phone:
                raise Conflict(ERROR_USER_PHONE_ALREADY_EXISTS)
            if email and user.email == email:
                raise Conflict(ERROR_USER_EMAIL_ALREADY_EXISTS)


def teacher_existe(db_session: Session, teacher_cpf: str) -> bool:

    register = db_session.scalar(
        select(UserModel).where(
            UserModel.cpf == teacher_cpf and
            UserModel.level == LEVEL["teacher"]
        )
    )

    return True if register else False


def class_existe(db_session: Session, class_name: str, class_section: str) -> bool:
    """
    Busca uma turma pelo nome e seção.

    - Args:
        - db_session: Sessão do banco de dados.
        - class_name: Nome da turma.
        - class_section: Seção da turma.

    - Returns:
        - bool: True se a turma existe, False caso contrário.
    """

    filters = (
        ClassModel.name == class_name,
        ClassModel.section == class_section,
    )

    register = db_session.scalar(
        select(ClassModel).where(
            and_(*filters))
    )

    return True if register else False


def class_event_existe(db_session: Session, request: ClassEventRequest) -> bool:
    """
    Verifica se um evento de uma turma existe.

    - Args:
        - db_session: Sessão do banco de dados.
        - class_id: ID da turma.
        - event_id: ID do evento.

    - Returns:
        - bool: True se o evento existe, False caso contrário.
    """

    filters = (
        ClassEventModel.class_id == request.class_id,
        ClassEventModel.discipline_id == request.disciplines_id,
        ClassEventModel.teacher_id == request.teacher_id,
        ClassEventModel.start_date == unformat_date(request.start_date) ,
        ClassEventModel.end_date == unformat_date(request.end_date),

    )

    return register_exists(db_session, ClassEventModel, filters)



def register_exists(db_session: Session, table: BaseModel, filters: tuple):
    """
    Verifica se um registro existe em uma tabela.

    - Args:
        - db_session: Sessão do banco de dados.
        - table: Modelo da tabela.
        - filters: Filtros para a busca.

    - Returns:
        - bool: True se o registro existe, False caso contrário.
    """

    register = db_session.scalar(
        select(table).where(
            and_(*filters))
    )

    return True if register else False


def generate_filters(table: BaseModel, attributes: list[str]) -> list:
    """
    Gera uma lista de filtros para a busca de um registro.

    - Args:
        - table: Modelo da tabela.
        - attributes: Atributos do registro.

    - Returns:
        - list: Lista de filtros.
    """

    filters = []

    for attribute in attributes:
        filters.append(getattr(table, attribute))

    return filters