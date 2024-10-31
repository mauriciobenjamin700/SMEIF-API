from sqlalchemy import select
from sqlalchemy.orm import Session


from database.models import(
    ChildModel,
    ClassStudantModel,
    ClassModel
)
from schemas.classes import(
    Student
)
from utils.messages import NotFoundErrorMessage
from constants.classes import (
    ERROR_CLASSES_GET_ALL_NOT_FOUND,
)


def get_all_studants_by_class(db_session: Session, class_id: str) -> list[Student]:
    
    relations = db_session.scalars(
        select(ClassStudantModel).where(
            ClassStudantModel.class_id == class_id
        )
    )

    children = db_session.scalars(
        select(ChildModel).join(
            ClassStudantModel,
            ChildModel.cpf == ClassStudantModel.child_cpf
        ).where(
            ClassStudantModel.id == class_id
        )
    )

    studants = []

    for child in children:

        studants.append(
            Student(
                cpf=child.cpf,
                name=child.name,
                matriculation=child.matriculation
            )
        )     

    return studants   


def get_all_classes(db_session: Session) -> list[ClassModel]:
    
    classes =  db_session.scalars(
        select(ClassModel)
    )

    if not classes:
        raise NotFoundErrorMessage(ERROR_CLASSES_GET_ALL_NOT_FOUND)