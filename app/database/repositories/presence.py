from sqlalchemy import select
from sqlalchemy.orm import Session


from database.models import (
    ClassEventModel, 
    PresenceModel
)
from schemas.classes import build_class_info

from schemas.presence import (
    PresenceRequest,
    PresenceDB,
    PresenceResponse
)
from utils.format import (
    format_data_utc_to_local, 
    format_date
)


class PresenceRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
        
    def add(self, model: PresenceModel) -> None:
        
        self.db_session.add(model)
        self.db_session.commit()
        
    
    def get(self, id: str) -> PresenceModel | None:
        return self.db_session.scalar(
            select(PresenceModel)
            .where(PresenceModel.id == id)
        )
        
            
    def get_by_child_cpf(self, child_cpf: str) -> list[PresenceModel]:
        return self.db_session.scalars(
            select(PresenceModel)
            .where(PresenceModel.child_cpf == child_cpf)
        ).all()
    
    def get_all(self) -> list[PresenceModel]:
        return self.db_session.scalars(
            select(PresenceModel)
        ).all()
    

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
    
    
    def map_model_to_response(self, model: PresenceModel) -> PresenceResponse:

        class_event:ClassEventModel = model.class_event

        duration = class_event.end_date - class_event.start_date 

        return PresenceResponse(
            **model.dict(exclude=["created_at"]),
            created_at=format_data_utc_to_local(model.created_at),
            date=format_date(class_event.start_date),
            duration=str(duration),
            class_info=build_class_info(class_event.class_)

        )
    
    
    def map_request_to_model(self, request: PresenceRequest) -> PresenceModel:
        
        to_db = PresenceDB(
            **request.dict(),
        )

        return PresenceModel(**to_db.dict())
