from pydantic import(
    Field,
    field_validator
)


from constants.base import ERROR_INVALID_CPF
from constants.teacher import (
    ERROR_TEACHER_INVALID_FIELD_CLASSES, 
    ERROR_TEACHER_INVALID_FIELD_DISCIPLINES, 
    ERROR_TEACHER_REQUIRED_FIELD_CLASSES, 
    ERROR_TEACHER_REQUIRED_FIELD_DISCIPLINES,
)
from schemas.base import BaseSchema
from schemas.classes import ClassResponse
from schemas.disciplines import DisciplineResponse
from schemas.user import UserResponse
from utils.format import (
    clean_string_field,
    unformat_cpf
)
from utils.messages.error import UnprocessableEntity
from utils.validate import (
    validate_cpf,
    validate_string
)


class TeacherDisciplinesRequest(BaseSchema):
    """
    - user_cpf: str
    - disciplines_id: list[str]
    """
    user_cpf: str = Field(
        title="CPF do Professor",
        description="CPF do professor fornecido no cadastro de usuário",
        examples=["123.456.789-09"]
    )
    disciplines_id: list[str] = Field(
        title="ID das Disciplinas",
        description="IDs das disciplinas que o professor ministra",
        examples=[['1', '2'], ['45','37']]
    )


    @field_validator("user_cpf", mode="before")
    def validate_teacher_cpf(cls, value) -> str:

        value = clean_string_field(value)

        if not validate_cpf(value):
            raise UnprocessableEntity(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)
    
    @field_validator("disciplines_id", mode="before")
    def validate_disciplines_id(cls, value) -> list[str]:

        if not isinstance(value, list):
            raise UnprocessableEntity(ERROR_TEACHER_INVALID_FIELD_DISCIPLINES)
        
        if not value:
            raise UnprocessableEntity(ERROR_TEACHER_REQUIRED_FIELD_DISCIPLINES)

        for discipline_id in value:
            if not validate_string(discipline_id):
                raise UnprocessableEntity(ERROR_TEACHER_INVALID_FIELD_DISCIPLINES)
        
        return value
    

class ClassTeacherRequest(BaseSchema):
    """
    - user_cpf: str
    - classes_id: list[str] 
    """

    user_cpf: str = Field(
        title="CPF do Professor",
        description="CPF do professor fornecido no cadastro de usuário",
        examples=["123.456.789-09"]
    )
    classes_id: list[str] = Field(
        title="ID das Turmas",
        description="IDs das turmas que o professor ministra",
        examples=["1", "2", "3"]
    )


    @field_validator("user_cpf", mode="before")
    def validate_teacher_cpf(cls, value) -> str:

        value = clean_string_field(value)

        if not validate_cpf(value):
            raise UnprocessableEntity(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)
    

    @field_validator("classes_id", mode="before")
    def validate_classes_id(cls, value) -> list[str]:

        if not isinstance(value, list):
            raise UnprocessableEntity(ERROR_TEACHER_INVALID_FIELD_CLASSES)
        
        if not value:
            raise UnprocessableEntity(ERROR_TEACHER_REQUIRED_FIELD_CLASSES)

        for class_id in value:
            if not validate_string(class_id):
                raise UnprocessableEntity(ERROR_TEACHER_INVALID_FIELD_CLASSES)
        
        return value
    

class TeacherResponse(BaseSchema):
    """
    - user: UserResponse
    - disciplines: list[DisciplineResponse]
    - classes: list[ClassResponse]
    """
    user: UserResponse = Field(
        title="Usuário",
        description="Informações do usuário que é professor"
    )
    disciplines: list[DisciplineResponse] = Field(
        title="Disciplinas",
        description="Disciplinas que o professor ministra aulas"
    )
    classes: list[ClassResponse] = Field(
        title="Turmas",
        description="Turmas que o professor ministra aulas"
    )