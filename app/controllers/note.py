from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.note import (
    ERROR_NOTE_NOT_FOUND,
    SUCCESS_NOTE_ADD,
    SUCCESS_NOTE_DELETE
)
from database.repositories.note import NoteRepository
from schemas.base import BaseMessage
from schemas.note import (
    NoteFilters,
    NoteRequest,
    NoteResponse,
    NoteUpdate
)
from utils.messages.error import(
    NotFound,
    Server
)
from utils.messages.success import Success


class NoteController:
    def __init__(self, db_session: Session):
        self.repository = NoteRepository(db_session)
        
    
    def add(self, request: NoteRequest):
        """
        Registra uma nova nota no banco de dados
        
        - Args:
            - request: Objeto com os dados da nova nota.
            
        - Returns:
            - Success: Mensagem de sucesso ao cadastrar a nova nota.
        """
        try:
            
            self.repository.validate_note(request)
            
            model = self.repository.map_request_to_model(request)
            
            self.repository.add(model)
            
            return Success(SUCCESS_NOTE_ADD)
            
        except HTTPException:
            
            raise
        
        except Exception as e:
            
            raise Server(e)
        
        
    def get_all(self, filters: NoteFilters) -> list[NoteResponse]:
        """
        Busca todas as notas cadastradas no banco de dados e retorna de acordo com os filtros passados
        
        - Args:
            - filters: Objeto com os filtros para busca.
            
        - Returns:
            - list[NoteResponse]: Lista de notas encontradas no banco de dados.
        """
        try:
            
            models = self.repository.get_all()
            
            for key, value in filters.dict().items():
                
                models = [model for model in models if getattr(model, key) == value]
            
            response = [self.repository.map_model_to_response(model) for model in models]
            
            return response
            
        except Exception as e:
            
            raise Server(e)
        
        
    def update(self, request: NoteUpdate) -> NoteResponse:
        """
        Atualiza uma nota no banco de dados
        
        - Args:
            - request: Objeto com os novos dados da nota.
            
        - Returns:
            - NoteResponse: Objeto com os dados da nota atualizada.
        """
        try:
            
            model = self.repository.get(request.id)
            
            if not model:
                raise NotFound(ERROR_NOTE_NOT_FOUND)
            
            for key, value in request.dict(exclude=["id"]).items():
                
                setattr(model, key, value)
                        
            model = self.repository.update(model)
            
            response = self.repository.map_model_to_response(model)
            
            return response
            
        except HTTPException:
            
            raise
        
        except Exception as e:
            
            raise Server(e)
        
        
    def delete(self, id: int) -> BaseMessage:
        """
        Deleta uma nota no banco de dados
        
        - Args:
            - id: ID da nota a ser deletada.
            
        - Returns:
            - Success: Mensagem de sucesso ao deletar a nota.
        """
        try:
            
            result = self.repository.delete(id)
            
            if not result:
                raise NotFound(ERROR_NOTE_NOT_FOUND)
            
            return Success(SUCCESS_NOTE_DELETE)
            
        except HTTPException:
            
            raise
        
        except Exception as e:
            
            raise Server(e)