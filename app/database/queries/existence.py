from sqlalchemy import (
    and_,
    or_,
    select
)
from sqlalchemy.orm import Session


from constants.user import (
    ERROR_USER_CPF_ALREADY_EXISTS,
    ERROR_USER_EMAIL_ALREADY_EXISTS,
    ERROR_USER_PHONE_ALREADY_EXISTS
)
from database.base import BaseModel
from database.models import (
    ClassEventModel,
    ClassTeacherModel,
    DisciplinesModel,
    RecurrencesModel,
    TeacherDisciplinesModel,
    UserModel,
    ClassModel
)
from schemas.base import UserLevel
from schemas.classes import ClassEventRequest, Recurrences
from utils.messages.error import Conflict



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
            UserModel.level == UserLevel.TEACHER.value
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

    filters = [
        ClassEventModel.class_id == request.class_id,
        ClassEventModel.teacher_id == request.teacher_id
    ]

    for discipline_id in request.disciplines_id:
        filters.append(ClassEventModel.discipline_id == discipline_id)
            

        #ClassEventModel.start_date == unformat_date(request.start_date, False) ,
        #ClassEventModel.end_date == unformat_date(request.end_date, False),

    return register_exists(db_session, ClassEventModel, filters)


def recurrences_exists(db_session, class_event_id, recurrence: Recurrences) -> bool:
    """
    Verifica se uma recorrência de um evento de turma existe.

    - Args:
        - db_session: Sessão do banco de dados.
        - class_event_id: ID do evento de turma.
        - recurrence: Recorrência.

    - Returns:
        - bool: True se a recorrência existe, False caso contrário.
    """

    filters = (
        RecurrencesModel.class_event_id == class_event_id,
        RecurrencesModel.day_of_week == recurrence.day_of_week,
        RecurrencesModel.start_time ==  recurrence.start_time,
        RecurrencesModel.end_time == recurrence.end_time,
    )

    return register_exists(db_session, RecurrencesModel, filters)


def discipline_exists(db_session, discipline_name) -> bool:
    """
    Verifica se uma disciplina existe.

    - Args:
        - db_session: Sessão do banco de dados.
        - discipline_name: Nome da disciplina.

    - Returns:
        - bool: True se a disciplina existe, False caso contrário.
    """

    filters = (
        DisciplinesModel.name == discipline_name,
    )

    return register_exists(db_session, DisciplinesModel, filters)


def teacher_classes_exists(db_session: Session, user_cpf: str, classes: list[str]) -> bool:
    """
    Verifica se um professor possui cadastro nas turmas.

    - Args:
        - db_session: Sessão do banco de dados.
        - user_cpf: CPF do professor.
        - classes: IDs das turmas.

    - Returns:
        - bool: True se o professor possui as turmas, False caso contrário.
    """

    assossiation = db_session.scalars(
        select(ClassTeacherModel).where(
            and_(ClassTeacherModel.user_cpf == user_cpf, ClassTeacherModel.class_id.in_(classes))
        )
    ).all()

    return True if assossiation else False


def teacher_disciplines_exists(db_session: Session, user_cpf: str, disciplines: list[str]) -> bool:
    """
    Verifica se um professor possui cadastro nas disciplinas.

    - Args:
        - db_session: Sessão do banco de dados.
        - user_cpf: CPF do professor.
        - disciplines: IDs das disciplinas.

    - Returns:
        - bool: True se o professor possui as disciplinas, False caso contrário.
    """

    assossiation = db_session.scalars(
        select(TeacherDisciplinesModel).where(
            and_(TeacherDisciplinesModel.user_cpf == user_cpf, TeacherDisciplinesModel.discipline_id.in_(disciplines))
        )
    ).all()

    return True if assossiation else False