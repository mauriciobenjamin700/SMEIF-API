from sqlalchemy import select
from sqlalchemy.orm import Session


from constants.user import ERROR_USER_NOT_FOUND_USERS
from database.models import(
    ChildModel,
    ClassStudentModel,
    ClassModel,
    UserModel
)
from schemas.classes import(
    Student
)
from utils.messages.error import NotFound
from constants.classes import (
    ERROR_CLASSES_GET_ALL_NOT_FOUND,
)


def get_all_users(db_session: Session) -> list[UserModel]:
        
    users = db_session.scalars(select(UserModel)).all()

    if not users:
        raise NotFound(ERROR_USER_NOT_FOUND_USERS)
    
    return users

def get_all_students_by_class(db_session: Session, class_id: str) -> list[Student]:
    
    relations = db_session.scalars(
        select(ClassStudentModel).where(
            ClassStudentModel.class_id == class_id
        )
    )

    children = db_session.scalars(
        select(ChildModel).join(
            ClassStudentModel,
            ChildModel.cpf == ClassStudentModel.child_cpf
        ).where(
            ClassStudentModel.id == class_id
        )
    )

    students = []

    for child in children:

        students.append(
            Student(
                cpf=child.cpf,
                name=child.name,
                matriculation=child.matriculation
            )
        )     

    return students   


def get_all_classes(db_session: Session) -> list[ClassModel]:
    
    classes =  db_session.scalars(
        select(ClassModel)
    )

    if not classes:
        raise NotFound(ERROR_CLASSES_GET_ALL_NOT_FOUND)