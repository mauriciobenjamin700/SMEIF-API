from fastapi import HTTPException
from sqlalchemy.orm import Session


from database.queries.validate_foreignkey import validate_class_events
from constants.classes import(
    ERROR_CLASS_ADD_CONFLICT,
    ERROR_CLASSES_EVENTS_ADD_CONFLICT,
    MESSAGE_CLASS_ADD_SUCCESS,
    MESSAGE_CLASS_DELETE_SUCCESS,
    MESSAGE_CLASS_EVENT_ADD_SUCCESS,
    MESSAGE_CLASS_EVENT_DELETE_SUCCESS,
)
from database.models import(
    ClassModel,
    ClassEventModel,
    RecurrencesModel
)
from database.queries.existence import (
    class_event_existe,
    class_existe,
)
from database.queries.get import (
    get_class_by_id,
    get_class_event_by_id,
    get_teacher_by_cpf
)
from database.queries.get_all import (
    get_all_class_events,
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
        
    
    def add_event(self, request: ClassEventRequest) -> BaseMessage:
        """
        Cadastra uma aula de uma turma no sistema

        - Args:
            - class_id: ID da turma a qual a aula será cadastrado.
            - request: Objeto com os dados da aula a ser cadastrado.

        - Returns:
            - BaseMessage: Mensagem de sucesso ou erro.
        """
        try:

            if class_event_existe(self.db_session, request):

                raise Conflict(ERROR_CLASSES_EVENTS_ADD_CONFLICT)
            
            validate_class_events(self.db_session, request.class_id, request.disciplines_id, request.teacher_id)

            model  = ClassEventModel(
                id=id_generate(),
                **request.dict()
            )

            self.db_session.add(model)

            for recurrence in request.recurrences:

                recurrence_model = self._Recurrence_to_Model(model.id, recurrence)

                self.db_session.add(recurrence_model)

            self.db_session.commit()

            return Success(MESSAGE_CLASS_EVENT_ADD_SUCCESS)
            
        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        

    def get_event(self, class_event_id: str) -> ClassEventResponse:
        try:
            model = get_class_event_by_id(class_event_id)

            return self._Model_to_ClassEventResponse(model)
        
        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    def get_all_events(self) -> list[ClassEventResponse]:

        try:

        
            models = get_all_class_events(self.db_session)

            return [self._Model_to_ClassEventResponse(model) for model in models]
        
        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    def update_event(self, class_event_id: str, request: ClassEventRequest) -> ClassEventResponse:
        
        try:

            model = get_class_event_by_id(class_event_id)

            for key, value in request.dict().items():
                if key == "recurrences": # TODO: Recorrências só podem ser adicionadas e removidas, não alteradas
                    continue
                setattr(model, key, value)

            self.db_session.commit()
            self.db_session.refresh(model)

            return self._Model_to_ClassEventResponse(model)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    def delete_event(self, class_event_id: str) -> BaseMessage:
        try:

            model = get_class_event_by_id(class_event_id)

            self.db_session.delete(model)

            self.db_session.commit()

            return Success(MESSAGE_CLASS_EVENT_DELETE_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        

    def add_recurrences(self, class_event_id: str, recurrences: list[Recurrences]) -> BaseMessage:
        pass

    def delete_recurrences(self, class_event_id: str, recurrences: list[Recurrences]) -> BaseMessage:
        pass

    def _Model_to_Response(self, model: ClassModel) -> ClassResponse:
        """
        Converte um objeto do tipo ClassModel para um objeto do tipo ClassResponse

        - Args:
            - model: Objeto do tipo ClassModel a ser convertido.

        - Returns:
            - ClassResponse: Objeto com os dados da turma convertidos.
        """
        class_events = get_all_class_events_from_class(self.db_session, model.id)

        if not class_events:

            class_events = []

        else:
    
            class_events = [
                self._Model_to_ClassEventResponse(event) 
                for event in class_events
            ]

                    

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
        """
        constrói a informação da turma para ser exibida na resposta
        """
        return f"{model.name} {model.section}"
    

    def _Recurrence_to_Model(self, class_event_id: str,recurrence: Recurrences) -> RecurrencesModel:
        """
        Convert um objeto do tipo Recurrences para um objeto do tipo RecurrencesModel

        - Args:
            - class_event_id: ID da aula a qual a recorrência pertence.
            - recurrence: Objeto do tipo Recurrences a ser convertido.
        
        - Returns:
            - RecurrencesModel: Objeto com os dados da recorrência convertidos.
        """
        return RecurrencesModel(
            id=id_generate(),
            class_event_id=class_event_id,
            day_of_week=recurrence.day_of_week,
            start_time=recurrence.start_time,
            end_time=recurrence.end_time
        )
    
    def _Model_to_Recurrence(self, model: RecurrencesModel) -> Recurrences:
        """
        Converte um objeto do tipo RecurrencesModel para um objeto do tipo Recurrences

        - Args:
            - model: Objeto do tipo RecurrencesModel a ser convertido.

        - Returns:
            - Recurrences: Objeto com os dados da recorrência convertidos.
        """
        return Recurrences(
            day_of_week=model.day_of_week,
            start_time=format_date(model.start_time),
            end_time=format_date(model.end_time)
        )
        
    def _Model_to_ClassEventResponse(self, model: ClassEventModel) -> ClassEventResponse:
        """
        Converte um objeto do tipo ClassEventModel para um objeto do tipo ClassEventResponse

        - Args:
            - model: Objeto do tipo ClassEventModel a ser convertido.

        - Returns:
            - ClassEventResponse: Objeto com os dados da aula convertidos.
        """
        return ClassEventResponse(
            id=model.id,
            class_id=model.class_id,
            disciplines_id=model.disciplines_id,
            teacher_id=model.teacher_id,
            start_date=format_date(model.start_date),
            end_date=format_date(model.end_date),
            teacher_name=model.teacher.user.name,
            discipline_name=model.discipline.name,
            recurrences=[
                self._Model_to_Recurrence(recurrence) 
                for recurrence in model.recurrences
            ]
        )