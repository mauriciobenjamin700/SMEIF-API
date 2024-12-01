from database.models import DisciplinesModel
from schemas.disciplines import DisciplineResponse


def map_DisciplinesModel_to_DisciplineResponse(discipline: DisciplinesModel) -> DisciplineResponse:
    return DisciplineResponse(
            **discipline.dict()
        )