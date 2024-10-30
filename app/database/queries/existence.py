from sqlalchemy import select
from sqlalchemy.orm import Session


from constants.user import LEVEL
from database.models import (
    UserModel,
    ClassModel
)


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