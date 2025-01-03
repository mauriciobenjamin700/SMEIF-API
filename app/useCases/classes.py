from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.classes import(
    ERROR_CLASS_ADD_CONFLICT,
    ERROR_CLASSES_EVENTS_ADD_CONFLICT,
    ERROR_CLASSES_EVENTS_ADD_RECURRENCES_CONFLICT,
    ERROR_CLASSES_EVENTS_GET_ALL_NOT_FOUND,
    MESSAGE_CLASS_ADD_SUCCESS,
    MESSAGE_CLASS_DELETE_SUCCESS,
    MESSAGE_CLASS_EVENT_ADD_SUCCESS,
    MESSAGE_CLASS_EVENT_DELETE_SUCCESS,
    MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS,
    MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS,
)
from database.mapping.classes import (
    build_class_info, 
    map_ClassEventModel_to_ClassEventResponse, 
    map_ClassModel_to_ClassResponse,
    map_Recurrence_to_RecurrencesModel, 
    map_RecurrencesModel_to_Recurrences
)
from database.models import(
    ClassModel,
    ClassEventModel,
    RecurrencesModel
)
from database.queries.existence import (
    class_event_existe,
    class_existe,
    recurrences_exists,
)
from database.queries.get import (
    get_class_by_id,
    get_class_event_by_id,
    get_recurrence_by_attributes
)
from database.queries.get_all import (
    get_all_class_events,
    get_all_classes, 
)
from database.queries.validate_foreignkey import validate_class_events
from schemas.base import BaseMessage
from schemas.classes import (
    ClassEventResponse,
    ClassRequest,
    ClassEventRequest,
    ClassResponse,
    Recurrences,
)
from services.generator.ids import id_generate
from utils.messages.success import Success
from utils.messages.error import(
    Conflict,
    NotFound,
    Server,
)


class ClassesUseCases():

    def __init__(self, db_session: Session) -> None:
        self. db_session = db_session

    
    def add(self, request: ClassRequest) -> BaseMessage:
        """
        Cadastra uma turma no sistema

        - Args:
            - request: Objeto com os dados da turma a ser cadastrada.

        - Returns:
            - BaseMessage: Mensagem de sucesso.

        - Raises:
            - HTTPException: 409 - Turma já cadastrada.
            - Exception: Erro no servidor.
        """
        try:
            
            if class_existe(self.db_session, request.name, request.section):
               raise Conflict(ERROR_CLASS_ADD_CONFLICT)


            model = ClassModel(
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

        - Raises:
            - HTTPException: 404 - Turma não encontrada.
            - Exception: Erro no servidor.
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

        - Raises:
            - HTTPException: 404 - Nenhuma turma encontrada.
            - Exception: Erro no servidor.
        """
        try:

            classes = get_all_classes(self.db_session)
            
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

        - Raises:
            - HTTPException: 404 - Turma não encontrada.
            - Exception: Erro no servidor.
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

        - Raises:
            - HTTPException: 404 - Turma não encontrada.
            - Exception: Erro no servidor.
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

        - Raises:
            - HTTPException: 409 - Aula já cadastrada.
            - Exception: Erro no servidor.
        """
        try:

            if class_event_existe(self.db_session, request):

                raise Conflict(ERROR_CLASSES_EVENTS_ADD_CONFLICT)
            
            validate_class_events(self.db_session, request.class_id, request.disciplines_id, request.teacher_id)

            for discipline_id in request.disciplines_id:

                model  = ClassEventModel(
                    id=id_generate(),
                    class_id=request.class_id,
                    discipline_id=discipline_id,
                    teacher_id=request.teacher_id,
                    start_date=request.start_date,
                    end_date=request.end_date
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
        """
        Busca uma turma a partir de seu ID

        - Args:
            - class_event_id: ID da aula a ser buscada.
        
        - Returns:
            - ClassEventResponse: Objeto com os dados da aula buscada.

        - Raises:
            - HTTPException: 404 - Aula não encontrada.
            - Exception: Erro no servidor.
        """
        try:
            model = get_class_event_by_id(self.db_session,class_event_id)

            return self._Model_to_ClassEventResponse(model)
        
        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    def get_all_events(self) -> list[ClassEventResponse]:
        """
        Busca todas as aulas cadastradas no sistema

        - Args:
            - None

        - Returns:
            - list[ClassEventResponse]: Lista de objetos com os dados das aulas cadastradas.

        - Raises:
            - HTTPException: 404 - Nenhuma aula encontrada.
            - Exception: Erro no servidor.
        """
        try:
            models = get_all_class_events(self.db_session)

            if not models:
                raise NotFound(ERROR_CLASSES_EVENTS_GET_ALL_NOT_FOUND)

            return [self._Model_to_ClassEventResponse(model) for model in models]
        
        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    def update_event(self, class_event_id: str, request: ClassEventRequest) -> ClassEventResponse:
        """
        Atualiza uma aula cadastrada no sistema

        - Args:
            - class_event_id: ID da aula a ser atualizada.
            - request: Objeto com os dados da aula a ser atualizada.

        - Returns:
            - ClassEventResponse: Objeto com os dados da aula atualizada.

        - Raises:
            - HTTPException: 404 - Aula não encontrada.
            - Exception: Erro no servidor.
        """
        try:

            print(type(request))

            model = get_class_event_by_id(self.db_session,class_event_id)

            for key, value in request.dict().items():
                if key == "recurrences":
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
        """
        Deleta uma aula do sistema

        - Args:
            - class_event_id: ID da aula a ser deletada.

        - Returns:
            - BaseMessage: Mensagem de sucesso ou erro.

        - Raises:
            - HTTPException: 404 - Aula não encontrada.
            - Exception: Erro no servidor.
        """
        try:

            model = get_class_event_by_id(self.db_session,class_event_id)

            self.db_session.delete(model)

            self.db_session.commit()

            return Success(MESSAGE_CLASS_EVENT_DELETE_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        

    def add_recurrences(self, class_event_id: str, recurrences: list[Recurrences]) -> BaseMessage:
        """
        Adiciona uma lista de recorrências para uma aula

        - Args:
            - class_event_id: ID da aula a qual as recorrências serão adicionadas.
            - recurrences: Lista de recorrências a serem adicionadas.

        - Returns:
            - BaseMessage: Mensagem de sucesso.

        - Raises:
            - HTTPException: 409 - Recorrências conflitantes durante o cadastro.
            - Exception: Erro no servidor.
        """
        try:

            model = get_class_event_by_id(self.db_session,class_event_id)

            for recurrence in recurrences:

                if recurrences_exists(self.db_session, model.id, recurrence):

                    raise Conflict(ERROR_CLASSES_EVENTS_ADD_RECURRENCES_CONFLICT)

                recurrence_model = self._Recurrence_to_Model(model.id, recurrence)

                self.db_session.add(recurrence_model)

            self.db_session.commit()

            return Success(MESSAGE_CLASSES_EVENTS_ADD_RECURRENCES_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    def delete_recurrences(self, class_event_id: str, recurrences: list[Recurrences]) -> BaseMessage:
        """
        Remove uma lista de recorrências de uma aula

        - Args:
            - class_event_id: ID da aula a qual as recorrências serão removidas.
            - recurrences: Lista de recorrências a serem removidas.

        - Returns:
            - BaseMessage: Mensagem de sucesso

        - Raises:
            - HTTPException: 404 - Recorrência não encontrada.
            - Exception: Erro no servidor.
        """
        try:

            for recurrence in recurrences:

                recurrence_model = get_recurrence_by_attributes(self.db_session, class_event_id ,recurrence)

                self.db_session.delete(recurrence_model)

            self.db_session.commit()

            return Success(MESSAGE_CLASSES_EVENTS_DELETE_RECURRENCES_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)


    def _Model_to_Response(self, model: ClassModel) -> ClassResponse:
        """
        Converte um objeto do tipo ClassModel para um objeto do tipo ClassResponse

        - Args:
            - model: Objeto do tipo ClassModel a ser convertido.

        - Returns:
            - ClassResponse: Objeto com os dados da turma convertidos.
        """
        return map_ClassModel_to_ClassResponse(self.db_session,model)
    

    def build_class_info(self, model: ClassModel) -> str:
        """
        constrói a informação da turma para ser exibida na resposta
        """
        return build_class_info(model)
    

    def _Recurrence_to_Model(self, class_event_id: str,recurrence: Recurrences) -> RecurrencesModel:
        """
        Convert um objeto do tipo Recurrences para um objeto do tipo RecurrencesModel

        - Args:
            - class_event_id: ID da aula a qual a recorrência pertence.
            - recurrence: Objeto do tipo Recurrences a ser convertido.
        
        - Returns:
            - RecurrencesModel: Objeto com os dados da recorrência convertidos.
        """
        return map_Recurrence_to_RecurrencesModel(class_event_id, recurrence)
    
    def _Model_to_Recurrence(self, model: RecurrencesModel) -> Recurrences:
        """
        Converte um objeto do tipo RecurrencesModel para um objeto do tipo Recurrences

        - Args:
            - model: Objeto do tipo RecurrencesModel a ser convertido.

        - Returns:
            - Recurrences: Objeto com os dados da recorrência convertidos.
        """
        return map_RecurrencesModel_to_Recurrences(model)
        
    def _Model_to_ClassEventResponse(self, model: ClassEventModel) -> ClassEventResponse:
        """
        Converte um objeto do tipo ClassEventModel para um objeto do tipo ClassEventResponse

        - Args:
            - model: Objeto do tipo ClassEventModel a ser convertido.

        - Returns:
            - ClassEventResponse: Objeto com os dados da aula convertidos.
        """
        return map_ClassEventModel_to_ClassEventResponse(model)