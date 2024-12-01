from fastapi import HTTPException
from sqlalchemy.orm import Session


from database.mapping.classes import map_ClassModel_to_ClassResponse
from database.mapping.discipline import map_DisciplinesModel_to_DisciplineResponse
from database.mapping.user import map_UserModel_to_UserResponse
from database.queries.get_all import get_all_classes_by_teacher, get_all_disciplines_by_teacher
from database.queries.get import get_teacher_by_cpf
from schemas.base import UserLevel
from schemas.teacher import(
    ClassTeacherRequest,
    TeacherDisciplinesRequest,
    TeacherResponse
)
from utils.messages.error import (
    NotFound, 
    Server
)


class TeacherController:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_teacher(self, user_cpf: str) -> TeacherResponse:
        try:

            user = get_teacher_by_cpf(self.db_session, user_cpf)

            disciplines = get_all_disciplines_by_teacher(self.db_session, user_cpf)

            classes = get_all_classes_by_teacher(self.db_session, user_cpf)

            TeacherResponse(
                user=map_UserModel_to_UserResponse(user),
                disciplines=[map_DisciplinesModel_to_DisciplineResponse(discipline) for discipline in disciplines],
                classes=[map_ClassModel_to_ClassResponse(self.db_session,c) for c in classes]
            )

        except HTTPException:
            raise


        except Exception as e:
            raise Server(e)