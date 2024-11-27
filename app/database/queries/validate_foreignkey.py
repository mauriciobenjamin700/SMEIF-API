from sqlalchemy.orm import Session


from constants.classes import (
    ERROR_CLASSES_GET_NOT_FOUND
)
from constants.disciplines import ERROR_DISCIPLINES_GET_NOT_FOUND
from constants.teacher import ERROR_TEACHER_GET_NOT_FOUND

from database.models import(
    ClassModel,
    ClassTeacherModel,
    DisciplinesModel
)
from utils.messages.error import NotFound


def validate_class_events(db_session: Session, class_id: str, discipline_id: str, teacher_id: str) -> None:
    
    if not db_session.query(ClassModel).filter(ClassModel.id == class_id).first():
        raise NotFound(ERROR_CLASSES_GET_NOT_FOUND)
    
    if not db_session.query(DisciplinesModel).filter(DisciplinesModel.id == discipline_id).first():
        raise NotFound(ERROR_DISCIPLINES_GET_NOT_FOUND)
    
    if not db_session.query(ClassTeacherModel).filter(ClassTeacherModel.id == teacher_id).first():
        raise NotFound(ERROR_TEACHER_GET_NOT_FOUND)