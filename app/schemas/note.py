from pydantic import (
    Field,
    field_validator
)


from constants.note import(
    ERROR_NOTE_REQUIRED_FIELD_POINTS,
    ERROR_NOTE_REQUIRED_FIELD_DISCIPLINES_ID,
    ERROR_NOTE_REQUIRED_FIELD_CLASS_ID,
    ERROR_NOTE_REQUIRED_FIELD_CHILD_CPF,
    ERROR_NOTE_INVALID_FIELD_POINTS,
)
from schemas.base import BaseSchema
from services.generator.ids import id_generate
from utils.format import (
    clean_string_field,
    unformat_cpf
)
from utils.messages.error import UnprocessableEntity
from utils.validate import (
    validate_cpf,
    validate_string
)


class NoteRequest(BaseSchema):
    """
    - aval_number: int
    - points: float
    - discipline_id: str
    - class_id: str
    - child_cpf: str
    """
    aval_number: int = Field(
        title="Número da avaliação",
        description="Número da avaliação a ser cadastrada, podendo ser a primeira, segunda, terceira e por ai vai",
        examples=[1, 2, 3]
    )
    points: float
    discipline_id: str
    class_id: str
    child_cpf: str
    
    
    @field_validator("points", mode="before")
    def validate_points(cls, value):
        
        if not isinstance(value, (int, float)):
            raise UnprocessableEntity(ERROR_NOTE_REQUIRED_FIELD_POINTS)
        
        if value < 0 or value > 10:
            raise UnprocessableEntity(ERROR_NOTE_INVALID_FIELD_POINTS)
        
        return value
    
    
    @field_validator("discipline_id", mode="before")
    def validate_discipline_id(cls, value):
        
        value = clean_string_field(value)
        
        if not validate_string(value):
            raise UnprocessableEntity(ERROR_NOTE_REQUIRED_FIELD_DISCIPLINES_ID)
        
        return value
    
    
    @field_validator("class_id", mode="before")
    def validate_class_id(cls, value):
        
        value = clean_string_field(value)
        
        if not validate_string(value):
            raise UnprocessableEntity(ERROR_NOTE_REQUIRED_FIELD_CLASS_ID)
        
        return value
    
    
    @field_validator("child_cpf", mode="before")
    def validate_child_cpf(cls, value):
        
        value = clean_string_field(value)
        
        if not validate_cpf(value):
            raise UnprocessableEntity(ERROR_NOTE_REQUIRED_FIELD_CHILD_CPF)
        
        value = unformat_cpf(value)
        
        return value
        
    
    
class NoteDB(NoteRequest):
    """
    - id: str
    - aval_number: int
    - points: float
    - discipline_id: str
    - class_id: str
    - child_cpf: str
    """
    id: str = Field(default_factory=id_generate)
