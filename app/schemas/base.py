from enum import Enum
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    def dict(self, exclude: list[str] = [],**kwargs) -> dict:
        """
        Mapeia os atributos do objeto para um dicionário, excluindo os atributos passados como argumento.

        Valores None também são excluídos.
        """
        result =  super().model_dump()
        result = {k: v for k, v in result.items() if v is not None and k not in exclude}


        for k,v in kwargs.items():

            if v is not None:

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


class Gender(str, Enum):
    MALE = 'M',
    FEMALE = 'F',
    OTHER = 'Z'


class Kinship(str, Enum):
    FATHER = "Pai"
    MOTHER = "Mãe"
    GRANDMOTHER = "Avô"
    GRANDFATHER = "Avó"
    UNCLE = "Tio"
    AUNT = "Tia"
    BROTHER = "Irmão"
    SISTER = "Irmã"
    COUSIN = "Primo(a)"
    RESPONSIBLE = "Responsável Legal"
    TUTOR = "Tutor(a)"
    STEPFATHER = "Padrasto"
    STEPMOTHER = "Madrasta"
    OTHER = "Outros"


class UserLevel(int, Enum):
    PARENT = 1
    TEACHER = 2
    COORDINATION = 3
    ADMIN = 4


class Shift(str, Enum):
    MORNING = "Matutino"
    AFTERNOON = "Vespertino"
    NIGHT = "Noturno"
    
    
class PresenceType(str, Enum):
    P = "P"
    F = "F"