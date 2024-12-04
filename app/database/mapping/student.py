from sqlalchemy.orm import Session


from database.queries.get import get_class_by_id
from database.mapping.classes import build_class_info
from database.models import ChildModel, ClassModel
from schemas.child import(
    StudentRequest,
    StudentResponse
)
from services.generator.matriculation import matriculation_generate
from utils.format import unformat_date


def map_StudentRequest_to_ChildModel(request: StudentRequest) -> ChildModel:
    
    return ChildModel(
        cpf = request.cpf,
        matriculation = matriculation_generate(),
        name = request.name,
        birth_date = unformat_date(request.birth_date, False),
        gender = request.gender,
        dependencies = request.dependencies,
        state = request.state,
        city = request.city,
        neighborhood = request.neighborhood,
        street = request.street,
        house_number = request.house_number,
        complement = request.complement,
    )


def map_ChildModel_to_StudentResponse(
    db_session: Session,
    model: ChildModel,
    class_id: str | ClassModel
) -> StudentResponse:
    
    if isinstance(class_id, ClassModel):
        class_ = class_id
    else:
        class_ = get_class_by_id(db_session, class_id)

    return StudentResponse(
        matriculation=model.matriculation,
        name=model.name,
        class_info = build_class_info(class_),
        shift=class_.shift
    )