from sqlalchemy import select
from sqlalchemy.orm import Session


from database.models import(
    ChildModel,
    ClassStudantModel
)
from schemas.classes import(
    Student
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

