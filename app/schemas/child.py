from email.policy import default
from re import M
from pydantic import Field


from schemas.address import Address
from schemas.base import (
    BaseSchema,
    Gender,
    Kinship,
)



class StudentRequest(BaseSchema):
    """
    - cpf: str
    - name: str
    - birth_date: str
    - gender: str
    - class_id: strclass_
    - address: Address
    - kinship: str
    - parent_cpf: str
    - complement: str
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
    birth_date: str = Field(
        title="Data de Nascimento",
        description="Data de nascimento do aluno",
        examples=["1990-01-01"]
    )
    gender: str = Field(
        title="Gênero",
        description="Gênero do aluno",
        examples=[
            Gender.MALE.value,
            Gender.FEMALE.value,
            Gender.OTHER.value
        ],
    )
    class_id: str = Field(
        title="ID da Turma",
        description="Código da Turma",
        examples=['1', '2', '3']
    )
    address: Address
    kinship: str = Field(
        title="Parentesco",
        description="Parentesco do aluno com o Responsável",
        examples=[
            Kinship.FATHER.value,
            Kinship.MOTHER.value,
            Kinship.GRANDMOTHER.value,
            Kinship.GRANDFATHER.value,
            Kinship.UNCLE.value,
            Kinship.AUNT.value,
            Kinship.BROTHER.value,
            Kinship.SISTER.value,
            Kinship.COUSIN.value,
            Kinship.RESPONSIBLE.value,
            Kinship.TUTOR.value,
            Kinship.STEPFATHER.value,
            Kinship.STEPMOTHER.value,
            Kinship.OTHER.value
        ]
    )
    parent_cpf: str = Field(
        title="CPF do Responsável",
        description="CPF do Responsável",
        examples=["123.456.789-00", "987.654.321-00"]
    )
    complement: str | None = Field(
        title="Necessidades especiais",
        description="Caso o aluno tenha alguma condição médica, alergia, ou necessidades de acompanhamento especial.",
        examples=["Autismo", "Intolerância a lactose", "Mudo", "Cadeirante"],
        default=None,
    )


class StudentResponse(BaseSchema):
    """
    - matriculation: str
    - name: str
    - class_info: str
    - shift: str
    """
    matriculation: str = Field(
        title="Matrícula",
        description="Número de matrícula do aluno",
        examples=["123456", "654321"]
    )
    name: str = Field(
        title="Nome",
        description="Nome do aluno",
        examples=["João", "Maria", "José"]
    )
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


class ChildRequest(BaseSchema):
    """
    - cpf: str
    - name: name
    - birth_date: str
    - gender: str
    - address: Address
    - dependencies: str | None
    """
    cpf: str = Field(
        title="CPF da criança",
        description="CPF da criança",
        examples=["123.456.789-00", "987.654.321-00"]
    )
    name: str = Field(
        title="Nome",
        description="Nome da criança",
        examples=["João", "Maria", "José"]
    )
    birth_date: str = Field(
        title="Data de Nascimento",
        description="Data de nascimento da criança",
        examples=["1990-01-02"]
    )
    gender: str = Field(
        title="Gênero",
        description="Gênero da criança",
        examples=[
            Gender.MALE.value,
            Gender.FEMALE.value,
            Gender.OTHER.value
        ],
    )
    address: Address
    dependencies: str | None = Field(
        title="Dependências",
        description="Dependências da criança",
        examples=["Autismo", "Intolerância a lactose", "Mudo", "Cadeirante"],
        default=None
    )