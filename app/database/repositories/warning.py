from datetime import datetime
from sqlalchemy.orm import Session


from database.models import WarningModel
from schemas.warning import (
    WarningRequest,
    WarningDB
)
from services.generator.ids import id_generate

class WarningRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
        
    def add(self, model: WarningModel) -> None:
        
        self.db_session.add(model)
        self.db_session.commit()
        
    
    def get(self, id: str) -> WarningModel | None:
        return self.db_session.query(WarningModel).filter(WarningModel.id == id).first()
        
            
    def get_by_parent_cpf(self, parent_cpf: str) -> list[WarningModel]:
        return self.db_session.query(WarningModel).filter(WarningModel.parent_cpf == parent_cpf).all()
    
    def get_all(self) -> list[WarningModel]:
        return self.db_session.query(WarningModel).all()
    

    def update(self, model: WarningModel) -> WarningModel:
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
    
    
    def map_model_to_response(self, model: WarningModel):
        pass
    
    
    def map_request_to_model(self, request: WarningRequest, file_path: str | None = None):
        
        to_db = WarningDB(
            id=id_generate(),
            date=datetime.now(),
            file_path=file_path,
            **request.dict(),
        )

        return WarningDB(**to_db.dict())
