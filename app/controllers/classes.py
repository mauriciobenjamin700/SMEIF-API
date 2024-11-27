from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.classes import(
    ERROR_CLASS_ADD_CONFLICT,
    ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID,
    MESSAGE_CLASS_ADD_SUCCESS,
    MESSAGE_CLASS_DELETE_SUCCESS,
    MESSAGE_CLASS_UPDATE_SUCCESS
)
from constants.user import(
    ERROR_USER_GET_TEACHER_NOT_FOUND,
)
from database.models import(
    ClassModel,
    ClassEventModel,
)
from database.queries.existence import (
    class_existe,
    generate_filters,
    register_exists,
    teacher_existe
)
from database.queries.get import (
    get_class_by_id,
    get_teacher_by_cpf
)
from database.queries.get_all import (
    get_all_class_events_from_class,
    get_all_classes, 
)
from schemas.base import BaseMessage
from schemas.classes import (
    ClassEventResponse,
    ClassRequest,
    ClassEventRequest,
    ClassResponse,
    Recurrences,
)
from services.generator.ids import id_generate
from utils.format import format_date
from utils.messages.success import Success
from utils.messages.error import(
    Conflict,
    NotFound,
    Server,
)


class ClassesController():

    def __init__(self, db_session: Session) -> None:
        self. db_session = db_session

    
    def add(self, request: ClassRequest) -> BaseMessage:
        """
        Cadastra uma turma no sistema

        - Args:
            - request: Objeto com os dados da turma a ser cadastrada.

        - Returns:
            - BaseMessage: Mensagem de sucesso ou erro.
        """
        try:
            
            if class_existe(self.db_session, request.name, request.section):
               raise Conflict(ERROR_CLASS_ADD_CONFLICT)


            model  = ClassModel(
                id=id_generate(),
                **request.dict()
            )

            self.db_session.add(model)
            self.db_session.commit()
            self.db_session.refresh(model)

            return Success(MESSAGE_CLASS_ADD_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)


    def get(self, class_id: str) -> ClassResponse:
        """
        Busca uma turma no sistema com base em seu ID

        - Args:
            - class_id: ID da turma a ser buscada.

        - Returns:
            - ClassResponse: Objeto com os dados da turma buscada.
        """
        try:

            model = get_class_by_id(self.db_session, class_id)

            return self._Model_to_Response(model)


        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        

    def get_all(self) -> list[ClassResponse]:
        """
        Busca todas as turmas cadastradas no sistema

        - Args:
            - None

        - Returns:
            - list[ClassResponse]: Lista de objetos com os dados das turmas cadastradas.
        """
        try:

            classes = get_all_classes(self.db_session)
            print(classes)
            return [self._Model_to_Response(model) for model in classes]

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        

    def update(self, class_id: str, request: ClassRequest) -> ClassResponse:
        """
        Atualiza os dados de uma turma no sistema

        - Args:
            - class_id: ID da turma a ser atualizada.
            - request: Objeto com os dados da turma a ser atualizada.

        - Returns:
            - ClassResponse: Objeto com os dados da turma atualizada.
        """
        try:

            model = get_class_by_id(self.db_session, class_id)

            for key, value in request.dict().items():
                setattr(model, key, value)

            self.db_session.commit()
            self.db_session.refresh(model)

            return self._Model_to_Response(model)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        

    def delete(self, class_id: str) -> BaseMessage:
        """
        Deleta uma turma do sistema

        - Args:
            - class_id: ID da turma a ser deletada.

        - Returns:
            - BaseMessage: Mensagem de sucesso ou erro.
        """
        try:

            model = get_class_by_id(self.db_session, class_id)

            self.db_session.delete(model)
            self.db_session.commit()

            return Success(MESSAGE_CLASS_DELETE_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        

    def _Model_to_Response(self, model: ClassModel) -> ClassResponse:

        class_events = get_all_class_events_from_class(self.db_session, model.id)

        if not class_events:

            class_events = []

        else:
    
            for event in class_events:

                class_events.append(
                    ClassEventResponse(
                        id=event.id,
                        class_id=event.class_id,
                        disciplines_id=event.disciplines_id,
                        teacher_id=event.teacher_id,
                        start_date=format_date(event.start_date),
                        end_date=format_date(event.end_date),
                        teacher_name=event.teacher.user.name,
                        discipline_name=event.discipline.name,
                        recurrences=[
                            Recurrences(**recurrence.dict()) 
                            for recurrence in event.recurrences
                        ]
                    )
                )

        response = ClassResponse(
            id=model.id,
            education_level=model.education_level,
            name=model.name,
            section=model.section,
            shift=model.shift,
            max_students=model.max_students,
            class_info=self._build_class_info(model), 
            class_events=class_events
        )

        return response
    

    def _build_class_info(self, model: ClassModel) -> str:
        return f"{model.name} {model.section}"