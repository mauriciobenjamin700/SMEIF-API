from sqlalchemy.orm import Session


from database.models import (
    ClassEventModel, 
    ClassModel, 
    RecurrencesModel
)
from database.queries.get_all import get_all_class_events_from_class
from schemas.classes import (
    ClassEventResponse, 
    ClassResponse, 
    Recurrences
)
from services.generator.ids import id_generate
from utils.format import format_date


def map_RecurrencesModel_to_Recurrences(model: RecurrencesModel) -> Recurrences:
    """
    Converte um objeto do tipo RecurrencesModel para um objeto do tipo Recurrences

    - Args:
        - model: Objeto do tipo RecurrencesModel a ser convertido.

    - Returns:
        - Recurrences: Objeto com os dados da recorrência convertidos.
    """
    return Recurrences(
        day_of_week=model.day_of_week,
        start_time=model.start_time,
        end_time=model.end_time
    )

def map_Recurrence_to_RecurrencesModel(class_event_id: str,recurrence: Recurrences) -> RecurrencesModel:
    """
    Convert um objeto do tipo Recurrences para um objeto do tipo RecurrencesModel

    - Args:
        - class_event_id: ID da aula a qual a recorrência pertence.
        - recurrence: Objeto do tipo Recurrences a ser convertido.
    
    - Returns:
        - RecurrencesModel: Objeto com os dados da recorrência convertidos.
    """
    return RecurrencesModel(
        id=id_generate(),
        class_event_id=class_event_id,
        day_of_week=recurrence.day_of_week,
        start_time=recurrence.start_time,
        end_time=recurrence.end_time
    )

def map_ClassEventModel_to_ClassEventResponse(model: ClassEventModel) -> ClassEventResponse:
    """
    Converte um objeto do tipo ClassEventModel para um objeto do tipo ClassEventResponse

    - Args:
        - model: Objeto do tipo ClassEventModel a ser convertido.

    - Returns:
        - ClassEventResponse: Objeto com os dados da aula convertidos.
    """
    return ClassEventResponse(
        id=model.id,
        class_id=model.class_id,
        disciplines_id=[model.discipline_id],
        teacher_id=model.teacher_id,
        start_date=format_date(model.start_date, False),
        end_date=format_date(model.end_date, False),
        teacher_name=model.teacher.user.name,
        discipline_name=model.discipline.name,
        recurrences=[
            map_RecurrencesModel_to_Recurrences(recurrence) 
            for recurrence in model.recurrences
        ]
    )


def build_class_info(model: ClassModel) -> str:
    """
    constrói a informação da turma para ser exibida na resposta
    """
    return f"{model.name} {model.section}"


def map_ClassModel_to_ClassResponse(db_session: Session,model: ClassModel) -> ClassResponse:
    """
        Converte um objeto do tipo ClassModel para um objeto do tipo ClassResponse

        - Args:
            - model: Objeto do tipo ClassModel a ser convertido.

        - Returns:
            - ClassResponse: Objeto com os dados da turma convertidos.
    """
    class_events = get_all_class_events_from_class(db_session, model.id)

    if not class_events:

        class_events = []

    else:

        class_events = [
            map_ClassEventModel_to_ClassEventResponse(event) 
            for event in class_events
        ]
        

    response = ClassResponse(
        id=model.id,
        education_level=model.education_level,
        name=model.name,
        section=model.section,
        shift=model.shift,
        max_students=model.max_students,
        class_info=build_class_info(model), 
        class_events=class_events
    )

    return response