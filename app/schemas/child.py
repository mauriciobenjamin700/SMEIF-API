"""
- DataClasses for Child
    - ChildRequest
    - ChildResponse
    - ChildUpdateRequest
"""
from pydantic import (
    Field,
    field_validator
)

from schemas.base import BaseSchema
from utils.validate import(
    base_validation,
    validate_cpf,
    validate_string_field
)


class ChildRequest(BaseSchema):
    """
    - cpf: str
    - name: str
    - matricula: str
    """
    cpf: str = Field(title="cpf", description="CPF do aluno", examples=["123.456.789-22"])
    name: str = Field(title="name", description="Nome do aluno", examples=["John Doe"])
    matriculation: str = Field(title="matriculation", description="Matricula do aluno")


    @field_validator("cpf", mode="before")
    def field_validate_cpf(cls, value) -> str:
        value = base_validation(value, "CPF")
        return validate_cpf(value)
    
    @field_validator("name", mode="before")
    def field_validate_name(cls, value) -> str:
        return base_validation(value, "Nome")
    
    @field_validator("matriculation", mode="before")
    def field_validate_matriculation(cls, value) -> str:
       return base_validation(value, "Matricula")
        
class ChildResponse(BaseSchema):
    """
    - cpf: str
    - name: str
    - matriculation: str
    """

    cpf: str = Field(title="cpf", description="CPF do usuário", examples=["123.456.789-00"])
    name: str = Field(title="name", description="Nome do usuário", examples=["John Doe"])
    matriculation: str = Field(title="matriculation", description="Matricula do aluno")

class ChildUpdateRequest(BaseSchema):
    """
    - name: str
    """
    name: str = Field(title="name", description="Nome do usuário", examples=["John Doe"], default=None)

    @field_validator("name", mode="before")
    def field_validate_name(cls, value) -> str:
        value =  validate_string_field(value)

        return value