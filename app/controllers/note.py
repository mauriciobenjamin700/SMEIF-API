from fastapi import HTTPException
from sqlalchemy.orm import Session


from database.repositories.note import NoteRepository
from schemas.note import (
    NoteRequest
)
from utils.messages.error import(
    Server
)


class NoteController:
    def __init__(self, db_session: Session):
        self.repository = NoteRepository(db_session)
        
    
    def add(self, request: NoteRequest):
        
        try:
            
        except HTTPException:
            
            raise
        
        except Exception as e:
            
            raise Server(e)