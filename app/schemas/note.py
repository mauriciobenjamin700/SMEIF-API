from pydantic import (
    Field,
    field_validator
)


from constants.base import ERROR_INVALID_CPF
from constants.note import(
    ERROR_NOTE_INVALID_FIELD_AVAL_NUMBER,
    ERROR_NOTE_REQUIRED_FIELD_AVAL_NUMBER,
    ERROR_NOTE_REQUIRED_FIELD_POINTS,
    ERROR_NOTE_REQUIRED_FIELD_DISCIPLINES_ID,
    ERROR_NOTE_REQUIRED_FIELD_CLASS_ID,
    ERROR_NOTE_REQUIRED_FIELD_CHILD_CPF,
    ERROR_NOTE_INVALID_FIELD_POINTS,
    ERROR_NOTE_REQUIRED_FIELD_SEMESTER,
    SEMESTERS,
    AVAL_NUMBERS
)
from schemas.base import (
    BaseSchema,
    Shift
)
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
    - semester: int
    - aval_number: int
    - points: float
    - discipline_id: str
    - class_id: str
    - child_cpf: str
    """
    semester: int = Field(
        title="Semestre",
        description="Semestre da avaliação, podendo ser de 1, 2 e 3",
        examples=SEMESTERS
    )
    aval_number: int = Field(
        title="Número da avaliação",
        description="Número da avaliação a ser cadastrada, podendo ser a primeira, segunda, terceira e por ai vai",
        examples=AVAL_NUMBERS
    )
    points: float = Field(
        title="Pontuação",
        description="Pontuação da avaliação, podendo ser de 0 a 10",
        examples=[0.0, 10.0]
    )
    discipline_id: str = Field(
        title="ID da disciplina",
        description="ID da disciplina a qual a nota pertence",
        examples=["123456"]
    )
    class_id: str = Field(
        title="ID da turma",
        description="ID da turma a qual a nota pertence",
        examples=["123456"]
    )
    child_cpf: str = Field(
        title="CPF do aluno",
        description="CPF do aluno a qual a nota pertence",
        examples=["123.456.789-01"]
    )
    
    
    @field_validator("semester", mode="before")
    def validate_semester(cls, value):
        
        if not value:
            raise UnprocessableEntity(ERROR_NOTE_REQUIRED_FIELD_SEMESTER)
        
        if value not in SEMESTERS:
            raise UnprocessableEntity(ERROR_NOTE_INVALID_FIELD_POINTS)
        
        return value
    
    
    @field_validator("aval_number", mode="before")
    def validate_aval_number(cls, value):
        
        if not value:
            raise UnprocessableEntity(ERROR_NOTE_REQUIRED_FIELD_AVAL_NUMBER)
        
        if value not in AVAL_NUMBERS:
            raise UnprocessableEntity(ERROR_NOTE_INVALID_FIELD_AVAL_NUMBER)
        
        return value
    
    
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

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_NOTE_REQUIRED_FIELD_CHILD_CPF)
        
        if not validate_cpf(value):
            raise UnprocessableEntity(ERROR_INVALID_CPF)
        
        value = unformat_cpf(value)
        
        return value
        
    
    
class NoteDB(NoteRequest):
    """
    - id: str
    - semester: int
    - aval_number: int
    - points: float
    - discipline_id: str
    - class_id: str
    - child_cpf: str
    """
    id: str = Field(
        default_factory=id_generate,
        frozen=True,
    )


class NoteFilters(BaseSchema):
    """
    - class_id: str | None
    - discipline_id: str | None
    - child_cpf: str | None
    - aval_number: int | None
    - semester: int | None
    """
    class_id: str | None = Field(
        title="ID da turma",
        description="ID da turma a ser filtrada",
        examples=["123456"],
        default=None
    )
    discipline_id: str | None = Field(
        title="ID da disciplina",
        description="ID da disciplina a ser filtrada",
        examples=["123456"],
        default=None
    )
    child_cpf: str | None = Field(
        title="CPF do aluno",
        description="CPF do aluno a ser filtrado",
        examples=["123.456.789-01"],
        default=None
    )
    aval_number: int | None = Field(
        title="Número da avaliação",
        description="Número da avaliação a ser filtrada",
        examples=AVAL_NUMBERS,
        default=None
    )
    semester: int | None = Field(
        title="Semestre",
        description="Semestre da avaliação a ser filtrada",
        examples=SEMESTERS,
        default=None
    )
    
    @field_validator("child_cpf", mode="before")
    def validate_child_cpf(cls, value):
        
        if value is not None:
        
            value = clean_string_field(value)
            
            if not validate_cpf(value):
                raise UnprocessableEntity(ERROR_INVALID_CPF)
            
            value = unformat_cpf(value)
        
        return value
    
    
class NoteResponse(NoteDB):
    """
    - id: str
    - semester: int
    - aval_number: int
    - points: float
    - discipline_id: str
    - class_id: str
    - child_cpf: str
    - student_name: str
    - matriculation: str
    - discipline_name: str
    - class_name: str
    """
    student_name: str = Field(
        title="Nome do estudante",
        description="Nome do estudante a qual a nota pertence",
        examples=["João da Silva"]
    )
    matriculation: str = Field(
        title="Matrícula do estudante",
        description="Matrícula do estudante a qual a nota pertence",
        examples=["123456"]
    )
    discipline_name: str = Field(
        title="Nome da disciplina",
        description="Nome da disciplina a qual a nota pertence",
        examples=["Matemática", "Português"]
    )
    class_name: str = Field(
        title="Nome da turma",
        description="Nome da turma a qual a nota pertence",
        examples=["5° Ano", "6° Ano", "Pre-I"]
    )
    class_section: str = Field(
        title="Seção da turma",
        description="Seção da turma a qual a nota pertence",
        examples=["A", "B"]
    )
    class_shift: Shift = Field(
        title="Turno",
        description="Turno da disciplina",
        examples=[Shift.MORNING.value, Shift.AFTERNOON.value, Shift.NIGHT.value]
    )
    
    
class NoteUpdate(BaseSchema):
    """
    - id: str
    - aval_number: int | None
    - points: float | None
    """
    id: str = Field(
        title="ID da nota",
        description="ID da nota a ser atualizada",
        examples=["123456"]
    )
    aval_number: int | None = Field(
        title="Número da avaliação",
        description="Número da avaliação a ser atualizada",
        examples=AVAL_NUMBERS,
        default=None
    )
    points: float | None = Field(
        title="Pontuação",
        description="Pontuação da avaliação, podendo ser de 0 a 10",
        examples=[0.0, 10.0],
        default=None
    )
    
    
    @field_validator("aval_number", mode="before")
    def validate_aval_number(cls, value):
        
        if value is not None:
        
            if value not in AVAL_NUMBERS:
                raise UnprocessableEntity(ERROR_NOTE_INVALID_FIELD_AVAL_NUMBER)
        
        return value
    
    
    @field_validator("points", mode="before")
    def validate_points(cls, value):
        
        if value is not None:
        
            if not isinstance(value, (int, float)):
                raise UnprocessableEntity(ERROR_NOTE_REQUIRED_FIELD_POINTS)
            
            if value < 0 or value > 10:
                raise UnprocessableEntity(ERROR_NOTE_INVALID_FIELD_POINTS)
        
        return value