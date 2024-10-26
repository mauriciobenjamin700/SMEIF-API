"""
- DataClasses for Parent
    - ParentRequest
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

class ParentRequest(BaseSchema):
    """
    - child_cpf: str
    """
    
    child_cpf:str = Field(title="child_cpf", description="CPF do aluno", examples=["08006715389"])
    
    @field_validator("cpf", mode="before")
    def field_validate_cpf(cls, value) -> str:
        value = base_validation(value, "CPF")
        return validate_cpf(value)
    
    
class PresenceResponse(BaseSchema):
    """
    - type: str
    - date: datetime
    """
    type = Field(title="type", description="Presença do aluno", examples=['P','F'])
    date = Field(title="date", description="Horario de inicio da aula")
    
def 
    
    
class NotifyResponse(BaseSchema):
    pass