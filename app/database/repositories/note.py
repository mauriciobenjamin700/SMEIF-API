from sqlalchemy import (
    and_,
    select
)
from sqlalchemy.orm import Session

from constants.child import ERROR_CHILD_GET_NOT_FOUND
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
    NoteDB,
    NoteResponse
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
                
        return NoteResponse(
            **model.dict(),
            student_name=model.child.name,
            matriculation=model.child.matriculation,
            discipline_name=model.discipline.name,
            class_name=model.class_.name,
            class_section=model.class_.section,
            class_shift=model.class_.shift
        )
    
    
    def map_request_to_model(self, request: NoteRequest) -> NoteModel:
                
        to_db = NoteDB(**request.dict())

        return NoteModel(**to_db.dict())
    
    
    def validate_note(self, note: NoteRequest):
        """
        Valida se a nota a ser cadastrada já existe para o aluno na turma e disciplina
        
        - Args:
            - note: Objeto do tipo NoteRequest a ser validado.
            
        - Raises:
            - Conflict: Nota já existe para o aluno nesta turma nesta disciplina.
            - NotFound: Aluno, turma ou disciplina não encontrados.
        """        
        model = self.db_session.scalar(
            select(NoteModel)
            .where(
                and_(
                    # NoteModel.aval_number == note.aval_number,
                    # NoteModel.points == note.points,
                    NoteModel.discipline_id == note.discipline_id,
                    NoteModel.class_id == note.class_id,
                    NoteModel.child_cpf == note.child_cpf,
                )
            )
        )


        if model: # Caso exista uma nota para este aluno nesta turma nesta disciplina
            if (
                model.aval_number == note.aval_number
                and 
                model.semester == note.semester
            ): # se for para a mesma nota, sobe conflito
                raise Conflict(ERROR_NOTE_ALREADY_ADD)
        
        else: # Caso seja a primeira nota, precisamos validar se os dados externos existem e estão corretos
        
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
                raise NotFound(ERROR_CHILD_GET_NOT_FOUND)
        