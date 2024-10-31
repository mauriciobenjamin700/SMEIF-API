from fastapi import HTTPException
from sqlalchemy.orm import Session


from base import Repository
from constants.classes import(
    ERROR_CLASS_ADD_CONFLICT,
    MESSAGE_CLASS_ADD_SUCESS
)
from constants.user import(
    ERROR_USER_GET_TEACHER_NOT_FOUND
)
from database.models import(
    ClassModel,
    ClassEventModel,
    ClassStudantModel
)
from database.queries.existence import (
    class_existe,
    teacher_existe
)
from database.queries.get import (
    get_class_by_id,
    get_teacher_by_cpf
)
from database.queries.get_all import get_all_studants_by_class
from schemas.base import BaseMessage
from schemas.classes import (
    ClassRequest,
    ClassEventRequest,
    ClassStudentRequest,
    ClassResponse
)
from services.ids import id_generate
from utils.messages import(
    NotFoundErrorMessage,
    ServerError,
    SucessMessage
)


class ClassesUseCases(Repository):

    def __init__(self, db_session: Session) -> None:
        self. db_session = db_session

    
    def add(self, request: ClassRequest) -> BaseMessage:

        try:

            if not teacher_existe(self.db_session, request.teacher_cpf):
                raise NotFoundErrorMessage(ERROR_USER_GET_TEACHER_NOT_FOUND)
            
            if class_existe(self.db_session, request.name):
                raise NotFoundErrorMessage(ERROR_CLASS_ADD_CONFLICT)


            model  = ClassModel(
                id=id_generate(),
                **request.dict()
            )

            self.db_session.add(model)
            self.db_session.commit()
            self.db_session.refresh(model)

            return SucessMessage(MESSAGE_CLASS_ADD_SUCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)


    def get(self, class_id: str) -> BaseMessage:

        try:

            model = get_class_by_id(self.db_session, class_id)

            return self._Model_to_Response(model)


        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)
        

    # def add(self, request: ClassRequest) -> BaseMessage:

    #     try:


    #     except HTTPException:
    #         raise

    #     except Exception as e:
    #         raise ServerError(e)
        

    def _Model_to_Response(self, model: ClassModel) -> ClassResponse:

        teacher = get_teacher_by_cpf(self.db_session, model.teacher_cpf)

        students = get_all_studants_by_class(
            self.db_session, 
            model.id
        )

        response = ClassResponse(
            id=model.id,
            name=model.name,
            room=model.room,
            teacher_cpf=model.teacher_cpf,
            teacher_name=teacher.name,
            teacher_phone=teacher.phone,
            teacher_email=teacher.email,
            students=students
        )

        return response