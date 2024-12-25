from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.note import (
    SUCCESS_NOTE_ADD
)
from database.repositories.note import NoteRepository
from schemas.note import (
    NoteRequest
)
from utils.messages.error import(
    Server
)
from utils.messages.success import Success


class NoteController:
    def __init__(self, db_session: Session):
        self.repository = NoteRepository(db_session)
        
    
    def add(self, request: NoteRequest):
        
        try:
            
            self.repository.validate_note(request)
            
            model = self.repository.map_request_to_model(request)
            
            self.repository.add(model)
            
            return Success(SUCCESS_NOTE_ADD)
            
        except HTTPException:
            
            raise
        
        except Exception as e:
            
            raise Server(e)
        
        
    def get_all():
        pass