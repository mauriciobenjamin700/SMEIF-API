from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session


from constants.parent import (
    MESSAGE_IN_SCHOOL_SUCESS,
    MESSAGE_IN_SCHOOL_FAIL,
    MESSAGE_IN_SCHOOL_NULL,
    PRESENCE_NO_REGISTER,
    SUCESS_ID_EXISTS,
    ERROR_CPF_ALREADY_EXISTS,
    ERROR_NOT_FOUND_CHILD, 
    ERROR_NOT_FOUND_USERS, 
    ERROR_NOT_ID, 
    MESSAGE_UPDATE_FAIL, 
    MESSAGE_UPDATE_SUCESS
)
from controllers.base import Repository
from database.models import ChildParentsModel, PresenceModel, ChildModel
from schemas.parent import (
    ParentRequest
)
from utils.cryptography import (
    crypto
)
from utils.messages import (
    ServerError,
    SucessMessage,
    ErrorMessage
)


class ParentUseCases():
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def check_child_in_school(self, request: ParentRequest) -> dict | HTTPException:
        if self._check_existence(cpf=request.child_cpf):
            raise ErrorMessage(404, ERROR_NOT_FOUND_CHILD)
        
        presence = self.db_session.query(PresenceModel).filter_by(child_cpf=request.child_cpf).order_by(desc(PresenceModel.date)).first()
        
        if presence and presence.date.date() == datetime.now().date():
            if presence.type == 'P':
                return SucessMessage(MESSAGE_IN_SCHOOL_SUCESS)
            elif presence.type == 'F':
                return SucessMessage(MESSAGE_IN_SCHOOL_FAIL)
            else:
                return SucessMessage(MESSAGE_IN_SCHOOL_NULL)
        else:
            return ErrorMessage(404, PRESENCE_NO_REGISTER)
        
    def check_child_presences(self, request: ParentRequest):
        pass
    
    def check_child_notes(self, request: ParentRequest):
        pass
    
    def check_notifies(self, request: ParentRequest):
        pass
        
    def _check_existence(self, cpf: str | None) -> None:
            
            if cpf:
            
                user = self.db_session.query(ChildModel).filter_by(cpf=cpf).first()
        
                return (user is None)