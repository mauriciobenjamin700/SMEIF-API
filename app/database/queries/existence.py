from sqlalchemy import (
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
from database.models import (
    UserModel,
    ClassModel
)
from utils.messages.error import Conflict


def check_user_existence(db_session: Session, cpf: str | None, phone: str | None, email: str | None) -> None:
    filters = []
    
    if cpf:
        filters.append(UserModel.cpf == cpf)
    if phone:
        filters.append(UserModel.phone == phone)
    if email:
        filters.append(UserModel.email == email)

    print(filters)
    
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
            UserModel.cpf == teacher_cpf &
            UserModel.level == LEVEL["teacher"]
        )
    )

    return True if register else False


def class_existe(db_session: Session, class_name: str) -> bool:

    register = db_session.scalar(
        select(ClassModel).where(
            ClassModel.name == class_name
        )
    )

    return True if register else False