from datetime import datetime
from sqlalchemy import (
    and_,
    or_,
    select
)
from sqlalchemy.orm import Session


from constants.classes import ERROR_CLASSES_GET_NOT_FOUND
from constants.disciplines import ERROR_DISCIPLINES_GET_NOT_FOUND
from constants.note import(
    ERROR_NOTE_ALREADY_ADD
)
from database.models import (
    ClassModel,
    ChildModel,
    DisciplinesModel,
    NoteModel
)
from schemas.note import (
    NoteRequest,
    NoteDB
)
from utils.messages.error import (
    Conflict,
    NotFound
)

class NoteRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
        
    def add(self, model: NoteModel) -> None:
        
        self.db_session.add(model)
        self.db_session.commit()
        
    
    def get(self, id: str) -> NoteModel | None:
        return self.db_session.query(NoteModel).filter(NoteModel.id == id).first()
        
            
    def get_by_child_cpf(self, child_cpf: str) -> list[NoteModel]:
        return self.db_session.query(NoteModel).filter(NoteModel.child_cpf == child_cpf).all()
    
    def get_all(self) -> list[NoteModel]:
        return self.db_session.query(NoteModel).all()
    

    def update(self, model: NoteModel) -> NoteModel:
        self.db_session.commit()
        self.db_session.refresh(model)
        return model
    
    
    def delete(self, id: str) -> bool:
        model = self.get(id)
        result = False
        if model:
            self.db_session.delete(model)
            self.db_session.commit()
            result = True
            
        return result
    
    
    def map_model_to_response(self, model: NoteModel):
        pass
    
    
    def map_request_to_model(self, request: NoteRequest, file_path: str | None = None):
        
        to_db = NoteDB(
            date=datetime.now(),
            file_path=file_path,
            **request.dict(),
        )

        return NoteDB(**to_db.dict())
    
    
    def __validate_note(self, note: NoteRequest):
        
        model = self.db_session.scalar(
            select(NoteModel)
            .where(
                and_(
                    NoteModel.aval_number == note.aval_number,
                    NoteModel.points == note.points,
                    NoteModel.discipline_id == note.discipline_id,
                    NoteModel.class_id == note.class_id,
                    NoteModel.child_cpf == note.child_cpf,
                )
            )
        )


        if model:
            raise Conflict(ERROR_NOTE_ALREADY_ADD)
        
        if self.db_session.scalar(
            select(DisciplinesModel)
            .where(DisciplinesModel.id == note.discipline_id)
        ) is None:
            raise NotFound(ERROR_DISCIPLINES_GET_NOT_FOUND)
        
        if self.db_session.scalar(
            select(ClassModel)
            .where(ClassModel.id == note.class_id)
        ) is None:
            raise NotFound(ERROR_CLASSES_GET_NOT_FOUND)
        
        if self.db_session.scalar(
            select(ChildModel)
            .where(ChildModel.cpf == note.child_cpf)
        ) is None:
            raise NotFound(ERROR_CLASSES_GET_NOT_FOUND)
        )