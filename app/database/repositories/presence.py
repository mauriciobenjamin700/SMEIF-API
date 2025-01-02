from datetime import datetime
from sqlalchemy.orm import Session


from database.models import PresenceModel
from schemas.presence import (
    PresenceRequest,
    PresenceDB
)
from services.generator.ids import id_generate

class PresenceRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
        
    def add(self, model: PresenceModel) -> None:
        
        self.db_session.add(model)
        self.db_session.commit()
        
    
    def get(self, id: str) -> PresenceModel | None:
        return self.db_session.query(PresenceModel).filter(PresenceModel.id == id).first()
        
            
    def get_by_child_cpf(self, child_cpf: str) -> list[PresenceModel]:
        return self.db_session.query(PresenceModel).filter(PresenceModel.child_cpf == child_cpf).all()
    
    def get_all(self) -> list[PresenceModel]:
        return self.db_session.query(PresenceModel).all()
    

    def update(self, model: PresenceModel) -> PresenceModel:
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
    
    
    def map_model_to_response(self, model: PresenceModel):
        pass
    
    
    def map_request_to_model(self, request: PresenceRequest, file_path: str | None = None):
        
        to_db = PresenceDB(
            id=id_generate(),
            date=datetime.now(),
            file_path=file_path,
            **request.dict(),
        )

        return PresenceDB(**to_db.dict())
