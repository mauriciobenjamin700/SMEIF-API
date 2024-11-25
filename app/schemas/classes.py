from pydantic import (
    Field,
    field_validator
)

from utils.format import (
    clean_string_field,
    format_phone, 
    unformat_cpf
)
from constants.base import ERROR_INVALID_CPF, ERROR_INVALID_EMAIL
from constants.classes import (
    ERROR_CLASSES_INVALID_FIELD_END_DATE,
    ERROR_CLASSES_INVALID_FIELD_START_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID,
    ERROR_CLASSES_REQUIRED_FIELD_END_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_NAME,
    ERROR_CLASSES_REQUIRED_FIELD_ROOM,
    ERROR_CLASSES_REQUIRED_FIELD_START_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF,
    ERROR_STUDENT_REQUIRED_FIELD_CPF,
    ERROR_STUDENT_REQUIRED_FIELD_MATRICULATION,
    ERROR_STUDENT_REQUIRED_FIELD_NAME,
    ERROR_STUDENT_TYPE
)
from schemas.base import (
    BaseSchema, 
    DaysOfWeek,
    EducationLevel,
    Shift
)
from utils.messages.error import UnprocessableEntity
from utils.validate import(
    validate_date,
    validate_email,
    validate_cpf,
)


class ClassRequest(BaseSchema):
    """
    - type_of_teaching: str
    - name: str
    - id: str
    - shift: str
    - max_students: int
    """
    type_of_teaching: EducationLevel = Field(
        title="Tipo",
        description="Tipo de ensino",
        examples=[EducationLevel.ELEMENTARY.value, EducationLevel.PRESCHOOL.value]
    )
    name: str = Field(
        title="Nome",
        description="Nome da turma a ser cadastrada",
        examples=["5° Ano", "6° Ano", "Pre-I"]
    )
    id: str = Field(
        title="Identificação da turma",
        description="Sigla de identificação da turma",
        examples=["A", "B", "C"]
    )
    shift: Shift = Field(
        title="Turno",
        description="Turno da disciplina",
        examples=[Shift.MORNING.value, Shift.AFTERNOON.value, Shift.NIGHT.value]
    )
    max_students: int = Field(
        title="Máximo de Alunos",
        description="Número máximo de alunos que podem ser matriculados na disciplina",
        examples=[20, 30, 40]
    )


    @field_validator(type_of_teaching)
    def validate_type_of_teaching(cls, value) -> EducationLevel:
        return value


class ClassRecurrences(BaseSchema):
    """
    - day_of_week: str
    - start_time: str
    - end_time: str
    """
    day_of_week: DaysOfWeek = Field(
        title="Dia da Semana",
        description="Dia da semana que a aula ocorrerá",
        examples=[
            DaysOfWeek.MONDAY.value, 
            DaysOfWeek.TUESDAY.value, 
            DaysOfWeek.WEDNESDAY.value,
            DaysOfWeek.THURSDAY.value,
            DaysOfWeek.FRIDAY.value,
            DaysOfWeek.SATURDAY.value,
            DaysOfWeek.SUNDAY.value
        ]
    )
    start_time: str = Field(
        title="Hora de Início",
        description="Hora de início da aula",
        examples=["08:00", "13:00"]
    )
    end_time: str = Field(
        title="Hora de Fim",
        description="Hora de encerramento da aula",
        examples=["12:00", "17:00"]
    )


class ClassEventRequest(BaseSchema):
    """
    - class_id: str
    - disciplines_id: str
    - teacher_id: str
    - start_date: str
    - end_date: str
    - recurrences: list[str]
    """

    class_id: str = Field(
        title="ID da Disciplina",
        description="Código da disciplina que terá uma aula agendada",
        examples=['1', '2', '3']
    )
    disciplines_id: str = Field(
        title="ID da Disciplina",
        description="Código da disciplina que terá uma aula agendada",
        examples=['1', '2', '3']
    )
    teacher_id: str = Field(
        title="ID do Professor",
        description="Código do professor que ministrará a aula",
        examples=['1', '2', '3']
    )
    start_date: str = Field(
        title="Data de Início",
        description="Data de início das aula",
        examples=["2024-07-01"]
    )
    end_date: str = Field(
        title="Data de Fim",
        description="Data de encerramento da aulas",
        examples=["2024-11-28"]
    )
    recurrences: list[ClassRecurrences]


class ClassResponse(ClassRequest):
    """
    
    """
    class_info: str = Field(
        title="Informações da Turma",
        description="Informações da turma",
        examples=["5° Ano A", "6° Ano B", "8° Ano C"]
    )
    shift: str = Field(
        title="Turno",
        description="Turno da disciplina",
        examples=["Matutino", "Vespertino", "Noturno"]
    )
    type_of_teaching: str = Field(
        title="Tipo",
        description="Tipo de ensino",
        examples=["Infantil", "Fundamental"]
    )

