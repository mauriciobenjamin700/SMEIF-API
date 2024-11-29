from pydantic import (
    Field,
    field_validator
)


from constants.classes import (
    ERROR_CLASSES_INVALID_FIELD_CLASS_EVENTS,
    ERROR_CLASSES_INVALID_FIELD_DAY_OF_WEEK,
    ERROR_CLASSES_INVALID_FIELD_EDUCATION_LEVEL,
    ERROR_CLASSES_INVALID_FIELD_END_DATE,
    ERROR_CLASSES_INVALID_FIELD_ID,
    ERROR_CLASSES_INVALID_FIELD_MAX_STUDENTS,
    ERROR_CLASSES_INVALID_FIELD_SHIFT,
    ERROR_CLASSES_INVALID_FIELD_START_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID,
    ERROR_CLASSES_REQUIRED_FIELD_DAY_OF_WEEK,
    ERROR_CLASSES_REQUIRED_FIELD_DISCIPLINES_ID,
    ERROR_CLASSES_REQUIRED_FIELD_EDUCATION_LEVEL,
    ERROR_CLASSES_REQUIRED_FIELD_END_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_ID,
    ERROR_CLASSES_REQUIRED_FIELD_MAX_STUDENTS,
    ERROR_CLASSES_REQUIRED_FIELD_NAME,
    ERROR_CLASSES_REQUIRED_FIELD_RECURRENCES,
    ERROR_CLASSES_REQUIRED_FIELD_SHIFT,
    ERROR_CLASSES_REQUIRED_FIELD_START_DATE,
    ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF,
    ERROR_CLASSES_REQUIRED_FIELD_TEACHER_NAME
)
from constants.disciplines import ERROR_DISCIPLINES_REQUIRED_FIELD_NAME
from schemas.base import (
    BaseSchema, 
    DaysOfWeek,
    EducationLevel,
    Shift
)
from utils.format import clean_string_field
from utils.messages.error import UnprocessableEntity
from utils.validate import(
    validate_date,
    validate_string,
    validate_time_format,
)


class ClassRequest(BaseSchema):
    """
    - education_level: str
    - name: str
    - section: str
    - shift: str
    - max_students: int
    """
    education_level: str = Field(
        title="Tipo de educação",
        description="Tipo de ensino daquele aluno",
        examples=[EducationLevel.ELEMENTARY.value, EducationLevel.PRESCHOOL.value]
    )
    name: str = Field(
        title="Nome",
        description="Nome da turma a ser cadastrada",
        examples=["5° Ano", "6° Ano", "Pre-I"]
    )
    section: str = Field(
        title="Identificação da turma",
        description="Sigla de identificação da turma",
        examples=["A", "B", "C"],
        max_length=1
    )
    shift: str = Field(
        title="Turno",
        description="Turno da disciplina",
        examples=[Shift.MORNING.value, Shift.AFTERNOON.value, Shift.NIGHT.value]
    )
    max_students: int = Field(
        title="Máximo de Alunos",
        description="Número máximo de alunos que podem ser matriculados na disciplina",
        examples=[20, 30, 40]
    )


    @field_validator("education_level", mode="before")
    def validate_education_level(cls, value) -> str:

        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_EDUCATION_LEVEL)
        

        if value not in EducationLevel.__dict__.values():
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_EDUCATION_LEVEL)
        
        return value
    

    @field_validator("name", mode="before")
    def validate_name(cls, value) -> str:

        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_NAME)

        return value
    

    @field_validator("section", mode="before")
    def validate_id(cls, value) -> str:
            
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_ID)
        
        if len(value)!= 1:
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_ID)

        return value
    

    @field_validator("shift", mode="before")
    def validate_shift(cls, value) -> str:

        value = clean_string_field(value)
            
        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_SHIFT)

        if value not in Shift.__dict__.values():
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_SHIFT)
        
        return value
    

    @field_validator("max_students", mode="before")
    def validate_max_students(cls, value) -> int:
            
        if not value:
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_MAX_STUDENTS)

        if not isinstance(value, int):
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_MAX_STUDENTS)
        
        if value <= 0:
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_MAX_STUDENTS)
        
        return value


class Recurrences(BaseSchema):
    """
    - day_of_week: str
    - start_time: str
    - end_time: str
    """
    day_of_week: str = Field(
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


    @field_validator("day_of_week", mode="before")
    def validate_day_of_week(cls, value) -> str:

        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_DAY_OF_WEEK)

        if value not in DaysOfWeek.__dict__.values():
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_DAY_OF_WEEK)
        
        return value


    @field_validator("start_time", mode="before")
    def validate_start_time(cls, value) -> str:
            
        value = clean_string_field(value)

        if not validate_string(value):

            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_START_DATE)

        if not validate_time_format(value):
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_START_DATE)

        return value
    

    @field_validator("end_time", mode="before")
    def validate_end_time(cls, value) -> str:
            
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_END_DATE)

        if not validate_time_format(value):
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_END_DATE)

        return value
    

class ClassEventRequest(BaseSchema):
    """
    - class_id: str
    - disciplines_id: list[str]
    - teacher_id: str
    - start_date: str
    - end_date: str
    - recurrences: list[Recurrences]
    """

    class_id: str = Field(
        title="ID da Disciplina",
        description="Código da turma que terá uma aula agendada",
        examples=['1', '2', '3']
    )
    disciplines_id: list[str] = Field(
        title="IDs das Disciplina",
        description="Código das disciplinas que terão aulas ministradas pelo professor durante o período designado",
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
    recurrences: list[Recurrences]


    @field_validator("class_id", mode="before")
    def validate_class_id(cls, value) -> str:
            
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID)

        return value
    

    @field_validator("disciplines_id", mode="before")
    def validate_disciplines_id(cls, values) -> list[str]:

        if isinstance(values, str):
            values = [values]

        result = []

        for value in values:
            
            value = clean_string_field(value)

            if not validate_string(value):
                raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_DISCIPLINES_ID)
            
            result.append(value)

        return result
    

    @field_validator("teacher_id", mode="before")
    def validate_teacher_id(cls, value) -> str:
            
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF)

        return value
    

    @field_validator("start_date", mode="before")
    def validate_start_date(cls, value) -> str:
            
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_START_DATE)

        if not validate_date(value):
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_START_DATE)

        return value
    

    @field_validator("end_date", mode="before")
    def validate_end_date(cls, value) -> str:
            
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_END_DATE)

        if not validate_date(value):
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_END_DATE)

        return value
    

    @field_validator("recurrences", mode="before")
    def validate_recurrences(cls, value) -> list[Recurrences]:
                
        if not value:
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_RECURRENCES)

        if not isinstance(value, list):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_RECURRENCES)

        
        return value


class ClassEventResponse(ClassEventRequest):
    """
    - id: str
    - class_id: str
    - disciplines_id: str
    - teacher_id: str
    - start_date: str
    - end_date: str
    - recurrences: list[Recurrences]
    - teacher_name: str
    - discipline_name: str
    """
    id: str = Field(
        title="ID da Aula",
        description="Código da aula",
        examples=['1', '2', '3']
    )
    teacher_name: str = Field(
        title="Nome do Professor",
        description="Nome do professor que ministrará a aula",
        examples=["Prof. Jane Doe", "Prof. John Smith", "Prof. Mary Johnson"]
    )
    discipline_name: str = Field(
        title="Nome da Disciplina",
        description="Nome da disciplina que terá uma aula",
        examples=["Matemática", "Português", "Geografia"]
    )


    @field_validator("teacher_name", mode="before")
    def validate_teacher_name(cls, value) -> str:
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_TEACHER_NAME)

        return value


    @field_validator("discipline_name", mode="before")
    def validate_discipline_name(cls, value) -> str:
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_DISCIPLINES_REQUIRED_FIELD_NAME)

        return value


class ClassResponse(ClassRequest):
    """
    - id: str
    - education_level: str
    - name: str
    - section: str
    - shift: str
    - max_students: int
    - class_info: str
    - class_events: list[ClassEventResponse]
    """
    id: str = Field(
        title="ID da Turma",
        description="Código da turma",
        examples=['1', '2', '3']
    )
    class_info: str = Field(
        title="Informações da Turma",
        description="Informações da turma",
        examples=["5° Ano A", "6° Ano B", "8° Ano C"]
    )
    class_events: list[ClassEventResponse]


    @field_validator("class_info", mode="before")
    def validate_class_info(cls, value) -> str:

        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CLASSES_REQUIRED_FIELD_NAME)

        return value
    

    @field_validator("class_events", mode="before")
    def validate_class_events(cls, value) -> list[ClassEventResponse]:  

        if not isinstance(value, list):
            
            raise UnprocessableEntity(ERROR_CLASSES_INVALID_FIELD_CLASS_EVENTS)
        
        return value