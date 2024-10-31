from fastapi import HTTPException
from sqlalchemy.orm import Session


from controllers.base import Repository
from schemas.base import BaseMessage
from schemas.classes import (
    ClassRequest,
    ClassEventRequest,
    ClassStudentRequest,
    ClassResponse
)


class ClassesUseCases(Repository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    