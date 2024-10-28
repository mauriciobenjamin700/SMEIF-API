from pydantic import (
    Field,
    field_validator
)


from app.utils.messages import ErrorMessage
from schemas.base import BaseSchema
from utils.validate import (
    base_validation,
    validate_date,
    validate_email,
    validate_phone_number,
    validate_cpf
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
        value = base_validation(value, "Nome")
        return value
    

    @field_validator("room", mode="before")
    def validate_room(cls, value):
        value = base_validation(value, "Sala")
        return value
    

    @field_validator("teacher_cpf", mode="before")
    def validate_teacher_cpf(cls, value):
        value = base_validation(value, "CPF do Professor")
        return validate_cpf(value)
    

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
        value = base_validation(value, "ID da Disciplina")
        return value
    

    @field_validator("start_date", mode="before")
    def validate_start_date(cls, value):
        value = base_validation(value, "Data de Início")
        value = validate_date(value)
        return value
    

    @field_validator("end_date", mode="before")
    def validate_end_date(cls, value):
        value = base_validation(value, "Data de Fim")
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
        value = base_validation(value, "ID da Disciplina")
        return value
    

    @field_validator("child_cpf", mode="before")
    def validate_child_cpf(cls, value):
        value = base_validation(value, "CPF do Aluno")
        return validate_cpf(value)
    

class Studant(BaseSchema):
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
        value = base_validation(value, "CPF")
        return validate_cpf(value)
    

    @field_validator("name", mode="before")
    def validate_name(cls, value):
        value = base_validation(value, "Nome")
        return value
    

    @field_validator("matriculation", mode="before")
    def validate_matriculation(cls, value):
        value = base_validation(value, "Matrícula")
        return value

class ClassResponse(ClassRequest):
    """
    - id: str
    - teacher_name: str
    - teacher_phone: str
    _ teacher_email: str
    - students: List[Studant]
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
    students: list[Studant] = Field(
        tittle="Alunos",
        description="Lista de alunos matriculados na disciplina",
        examples=["[{cpf: '123.456.789-00', name: 'João', matriculation: '123456'}, {cpf: '987.654.321-00', name: 'Maria', matriculation: '654321'}]"]
    )


    @field_validator("teacher_phone", mode="before")
    def validate_teacher_phone(cls, value):
        value = base_validation(value)
        value = validate_phone_number(value)
        return value
    

    @field_validator("teacher_email", mode="before")
    def validate_teacher_email(cls, value):
        value = base_validation(value)
        return validate_email(value)


    @field_validator("students", mode="before")
    def validate_students(cls, value):
        if not value:
            return []
        
        for student in value:
            if not isinstance(student, Studant):
                raise ErrorMessage(400, "Aluno deve ser uma instância de Studant")
        
        return value