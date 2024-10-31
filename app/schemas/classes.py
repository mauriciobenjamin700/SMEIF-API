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
from schemas.base import BaseSchema
from utils.messages import ValidationErrorMessage
from utils.validate import(
    validate_date,
    validate_email,
    validate_phone_number,
    validate_cpf,
    validate_string
)


class ClassRequest(BaseSchema):
    """
    - name: str
    - room: str
    - teacher_cpf: str
    """
    name: str = Field(
        title="Nome",
        description="Nome da disciplina a ser cadastrada",
        examples=["Matemática", "Português", "Física"]
    )
    room: str = Field(
        title="Sala",
        description="Sala onde a aula será ministrada",
        examples=["Sala 01", "Sala 02", "Sala 03"]
    )
    teacher_cpf: str = Field(
        title="CPF do Professor",
        description="CPF do professor que ministrará a disciplina",
        examples=["123.456.789-00", "987.654.321-00"]
    )


    @field_validator("name", mode="before")
    def validate_name(cls, value):

        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_CLASSES_REQUIRED_FIELD_NAME)
        
        return value
    

    @field_validator("room", mode="before")
    def validate_room(cls, value):

        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_CLASSES_REQUIRED_FIELD_ROOM)
        
        return value
    

    @field_validator("teacher_cpf", mode="before")
    def validate_teacher_cpf(cls, value):

        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF)
        
        if not validate_cpf(value):

            raise ValidationErrorMessage(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)
    

class ClassEventRequest(BaseSchema):
    """
    - class_id: str
    - start_date: str # YYYY-MM-DD HH:MM
    - end_date: str # YYYY-MM-DD HH:MM
    """

    class_id: str = Field(
        title="ID da Disciplina",
        description="Código da disciplina que terá uma aula agendada",
        examples=['1', '2', '3']
    )
    start_date: str = Field(
        title="Data de Início",
        description="Data de início da aula",
        examples=["2021-01-01 08:00", "2021-01-01 14:00"]
    )
    end_date: str = Field(
        title="Data de Fim",
        description="Data de encerramento da aula",
        examples=["2021-01-01 10:00", "2021-01-01 16:00"]
    )


    @field_validator("class_id", mode="before")
    def validate_class_id(cls, value):
        
        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID)

        return value
    

    @field_validator("start_date", mode="before")
    def validate_start_date(cls, value):

        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_CLASSES_REQUIRED_FIELD_START_DATE)
        
        if not validate_date(value):

            raise ValidationErrorMessage(ERROR_CLASSES_INVALID_FIELD_START_DATE)

        value = validate_date(value)

        return value
    

    @field_validator("end_date", mode="before")
    def validate_end_date(cls, value):

        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_CLASSES_REQUIRED_FIELD_END_DATE)
        
        if not validate_date(value):

            raise ValidationErrorMessage(ERROR_CLASSES_INVALID_FIELD_END_DATE)

        value = validate_date(value)

        return value

class ClassStudentRequest(BaseSchema):
    """
    - class_id: str
    - child_cpf: str
    """

    class_id: str = Field(
        title="ID da Disciplina",
        description="Código da disciplina",
        examples=['1', '2', '3']
    )
    child_cpf: str = Field(
        title="CPF do Aluno",
        description="CPF do aluno que será matriculado na disciplina",
        examples=["123.456.789-00", "987.654.321-00"]
    )


    @field_validator("class_id", mode="before")
    def validate_class_id(cls, value):

        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_CLASSES_REQUIRED_FIELD_CLASS_ID)

        return value
    

    @field_validator("child_cpf", mode="before")
    def validate_child_cpf(cls, value):

        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_CLASSES_REQUIRED_FIELD_TEACHER_CPF)
        
        if not validate_cpf(value):

            raise ValidationErrorMessage(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)
    

class Student(BaseSchema):
    """
    - cpf: str
    - name: str
    - matriculation: str
    """

    cpf: str = Field(
        title="CPF",
        description="CPF do aluno",
        examples=["123.456.789-00", "987.654.321-00"]
    )
    name: str = Field(
        title="Nome",
        description="Nome do aluno",
        examples=["João", "Maria", "José"]
    )
    matriculation: str = Field(
        title="Matrícula",
        description="Matrícula do aluno",
        examples=["123456", "654321"]
    )


    @field_validator("cpf", mode="before")
    def validate_cpf(cls, value):
        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_STUDENT_REQUIRED_FIELD_CPF)
        return validate_cpf(value)
    

    @field_validator("name", mode="before")
    def validate_name(cls, value):
        
        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_STUDENT_REQUIRED_FIELD_NAME)
        
        return value
    

    @field_validator("matriculation", mode="before")
    def validate_matriculation(cls, value):
        
        value = clean_string_field(value)

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_STUDENT_REQUIRED_FIELD_MATRICULATION)

        return value

class ClassResponse(ClassRequest):
    """
    - id: str
    - teacher_name: str
    - teacher_phone: str
    _ teacher_email: str
    - students: List[Student]
    """
    id: str = Field(
        title="ID",
        description="Código da disciplina",
        examples=['1', '2', '3']
    )
    teacher_name: str = Field(
        title="Nome do Professor",
        description="Nome do professor que ministrará a disciplina",
        examples=["João", "Maria", "José"]
    )
    teacher_phone: str = Field(
        title="Telefone do Professor",
        description="Telefone do professor que ministrará a disciplina",
        examples=["(11) 91234-5678", "(11) 98765-4321"]
    )
    teacher_email: str = Field(
        title="E-mail do Professor",
        description="E-mail do professor que ministrará a disciplina",
        examples=["jose@gmail.com", "maria@gmail.com"]
    )
    students: list[Student] = Field(
        tittle="Alunos",
        description="Lista de alunos matriculados na disciplina",
        examples=["[{cpf: '123.456.789-00', name: 'João', matriculation: '123456'}, {cpf: '987.654.321-00', name: 'Maria', matriculation: '654321'}]"]
    )


    @field_validator("teacher_phone", mode="before")
    def validate_teacher_phone(cls, value):

        value = format_phone(value)
        return value
    

    @field_validator("teacher_email", mode="before")
    def validate_teacher_email(cls, value):
        
        if not validate_email(value):
            raise ValidationErrorMessage(ERROR_INVALID_EMAIL)

        return value


    @field_validator("students", mode="before")
    def validate_students(cls, value):
        if not value:
            return []
        
        for student in value:
            if not isinstance(student, Student):
                raise ValidationErrorMessage(ERROR_STUDENT_TYPE)
        
        return value