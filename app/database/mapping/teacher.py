from sqlalchemy.orm import Session


from constants.user import ERROR_USER_INVALID_TEACHER_LEVEL
from database.mapping.classes import map_ClassModel_to_ClassResponse
from database.mapping.discipline import map_DisciplinesModel_to_DisciplineResponse
from database.mapping.user import map_UserModel_to_UserResponse
from database.models import UserModel
from database.queries.get_all import (
    get_all_classes_by_teacher, 
    get_all_disciplines_by_teacher
)
from schemas.base import UserLevel
from schemas.teacher import TeacherResponse
from utils.messages.error import BadRequest


def map_UserModel_to_TeacherResponse(db_session: Session, user: UserModel) -> TeacherResponse:

    if user.level != UserLevel.TEACHER.value:

        BadRequest(ERROR_USER_INVALID_TEACHER_LEVEL)

    disciplines = get_all_disciplines_by_teacher(db_session, user.cpf)

    classes = get_all_classes_by_teacher(db_session, user.cpf)

    return TeacherResponse(
        user=map_UserModel_to_UserResponse(user),
        disciplines=[map_DisciplinesModel_to_DisciplineResponse(discipline) for discipline in disciplines],
        classes=[map_ClassModel_to_ClassResponse(db_session,c) for c in classes]
    )