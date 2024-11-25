from enum import Enum
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    def dict(self, **kwargs) -> dict:
        result =  super().model_dump()
        result = {k: v for k, v in result.items() if v is not None}

        for k,v in kwargs.items():
            result[k] = v
        return result


class BaseMessage(BaseSchema):
    detail: str


class DaysOfWeek(str, Enum):
    MONDAY = "Segunda"
    TUESDAY = "Terça"
    WEDNESDAY = "Quarta"
    THURSDAY = "Quinta"
    FRIDAY = "Sexta"
    SATURDAY = "Sábado"
    SUNDAY = "Domingo"


class EducationLevel(str, Enum):
    PRESCHOOL = "Infantil"
    ELEMENTARY = "Fundamental"


class Shift(str, Enum):
    MORNING = "Matutino"
    AFTERNOON = "Vespertino"
    NIGHT = "Noturno"