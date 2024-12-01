from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.teacher import (
    ERROR_TEACHER_ADD_CLASSES_CONFLICT, 
    ERROR_TEACHER_ADD_DISCIPLINES_CONFLICT
)
from database.mapping.teacher import map_UserModel_to_TeacherResponse
from database.models import (
    ClassTeacherModel, 
    TeacherDisciplinesModel
)
from database.queries.existence import (
    teacher_classes_exists, 
    teacher_disciplines_exists
)
from database.queries.get_all import (
    get_all_class_teacher_models_by_filter, 
    get_all_teacher_disciplines_by_filter, 
    get_all_teachers
)
from database.queries.get import get_teacher_by_cpf
from services.generator.ids import id_generate
from schemas.teacher import(
    ClassTeacherRequest,
    TeacherDisciplinesRequest,
    TeacherResponse
)
from utils.messages.error import (
    Conflict,
    Server
)


class TeacherController:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def add_classes(self, request: ClassTeacherRequest) -> TeacherResponse:
        """
        Adiciona disciplinas ao professor

        - Args:
            - request: Dados da requisição

        - Returns:
            - TeacherResponse: Dados do professor
        """

        try:
            user = get_teacher_by_cpf(self.db_session, request.user_cpf)


            if teacher_classes_exists(self.db_session, request.user_cpf, request.classes_id):

                raise Conflict(ERROR_TEACHER_ADD_CLASSES_CONFLICT)
            
            classes = [
                ClassTeacherModel(
                    id=id_generate(),
                    user_cpf=request.user_cpf,
                    class_id=class_id
                ) for class_id in request.classes_id
            ]
        
            self.db_session.add_all(classes)
            self.db_session.commit()

            return map_UserModel_to_TeacherResponse(self.db_session, user)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)


    def add_disciplines(self, request: TeacherDisciplinesRequest) -> TeacherResponse:
        """
        Adiciona disciplinas ao professor

        - Args:
            - request: Dados da requisição

        - Returns:
            - TeacherResponse: Dados do professor
        """

        try:
            user = get_teacher_by_cpf(self.db_session, request.user_cpf)

            if teacher_disciplines_exists(self.db_session, request.user_cpf, request.disciplines_id):

                raise Conflict(ERROR_TEACHER_ADD_DISCIPLINES_CONFLICT)

            disciplines = [
                TeacherDisciplinesModel(
                    id=id_generate(),
                    user_cpf=request.user_cpf,
                    discipline_id=discipline_id
                ) for discipline_id in request.disciplines_id
            ]
        
            self.db_session.add_all(disciplines)

            self.db_session.commit()

            return map_UserModel_to_TeacherResponse(self.db_session, user)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        

    def get(self, user_cpf: str) -> TeacherResponse:
        """
        Busca um professor no banco de dados

        - Args:
            - user_cpf: CPF do professor

        - Returns:
            - TeacherResponse: Objeto com os dados do professor.
        
        """
        try:

            user = get_teacher_by_cpf(self.db_session, user_cpf)

            return map_UserModel_to_TeacherResponse(self.db_session, user)

        except HTTPException:
            raise


        except Exception as e:
            raise Server(e)
        
    
    def get_all(self) -> list[TeacherResponse]:
        """
        Busca todos os professores cadastrados

        - Args:
            - None

        - Returns:
            - list[TeacherResponse]: Lista de professores cadastrados
        """

        try:
            teachers = get_all_teachers(self.db_session)

            return [map_UserModel_to_TeacherResponse(self.db_session, teacher) for teacher in teachers]

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)


    def delete_classes(self, request: ClassTeacherRequest) -> TeacherResponse:
        """
        Remove turmas de um professor

        - Args:
            - user_cpf: CPF do professor
            - classes_id: Lista de IDs das turmas

        - Returns:
            - TeacherResponse: Dados do professor
        """

        try:

            user = get_teacher_by_cpf(self.db_session, request.user_cpf)

            assossiation =  get_all_class_teacher_models_by_filter(self.db_session, request.user_cpf, request.classes_id)

            for association in assossiation:
                self.db_session.delete(association)

            self.db_session.commit()

            return map_UserModel_to_TeacherResponse(self.db_session, user)
        

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        


    def delete_disciplines(self, request: TeacherDisciplinesRequest) -> TeacherResponse:
        """
        Remove disciplinas de um professor

        - Args:
            - user_cpf: CPF do professor
            - disciplines_id: Lista de IDs das disciplinas

        - Returns:
            - TeacherResponse: Dados do professor
        """

        try:

            user = get_teacher_by_cpf(self.db_session, request.user_cpf)

            assossiation =  get_all_teacher_disciplines_by_filter(self.db_session, request.user_cpf, request.disciplines_id)

            for association in assossiation:
                self.db_session.delete(association)

            self.db_session.commit()

            return map_UserModel_to_TeacherResponse(self.db_session, user)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)