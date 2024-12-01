from pydantic import (
    Field,
    field_validator
)


from constants.disciplines import ERROR_DISCIPLINES_REQUIRED_FIELD_NAME
from schemas.base import BaseSchema
from utils.format import clean_string_field
from utils.validate import validate_string
from utils.messages.error import UnprocessableEntity


class DisciplineRequest(BaseSchema):
    """
    - name: str
    """
    name: str = Field(
        title="Nome",
        description="Nome da disciplina",
        examples=["Matemática", "Português", "Geografia"]
    )


    @field_validator("name", mode="before")
    def validate_name(cls, value) -> str:

        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(
                ERROR_DISCIPLINES_REQUIRED_FIELD_NAME
            )
        
        return value


class DisciplineResponse(BaseSchema):
    """
    - id: str
    - name: str
    """
    id: str = Field(
        title="ID",
        description="Identificador da disciplina",
        example="1234567890"
    )
    name: str = Field(
        title="Nome",
        description="Nome da disciplina",
        example="Matemática"
    )