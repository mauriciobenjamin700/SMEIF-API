from pydantic import (
    Field,
    field_validator
)


from constants.base import(
ERROR_INVALID_CPF, 
ERROR_INVALID_FORMAT_BIRTH_DATE, 
ERROR_INVALID_FORMAT_GENDER,
ERROR_INVALID_FORMAT_SHIFT
)
from constants.child import (
    ERROR_CHILD_INVALID_FIELD_BIRTH_DATE,
    ERROR_CHILD_INVALID_FIELD_KINSHIP,
    ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE,
    ERROR_CHILD_REQUIRED_FIELD_CLASS_ID,
    ERROR_CHILD_REQUIRED_FIELD_CPF,
    ERROR_CHILD_REQUIRED_FIELD_GENDER,
    ERROR_CHILD_REQUIRED_FIELD_KINSHIP,
    ERROR_CHILD_REQUIRED_FIELD_NAME,
    ERROR_CHILD_REQUIRED_FIELD_PARENT_CPF,
)
from schemas.address import Address
from schemas.base import (
    BaseSchema,
    Gender,
    Kinship,
    Shift,
)
from utils.format import(
    clean_string_field,
    unformat_cpf
)
from utils.messages.error import UnprocessableEntity
from utils.validate import(
    is_adult,
    validate_cpf,
    validate_date,
    validate_string
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
    - dependencies: str | None
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
    gender: Gender = Field(
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
    kinship: Kinship = Field(
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
    dependencies: str | None = Field(
        title="Necessidades especiais",
        description="Caso o aluno tenha alguma condição médica, alergia, ou necessidades de acompanhamento especial.",
        examples=["Autismo", "Intolerância a lactose", "Mudo", "Cadeirante"],
        default=None,
    )


    @field_validator("cpf", mode="before")
    def validate_cpf(cls, value) -> str:

        value = value.strip()

        if not value:
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_CPF)

        if not validate_cpf(value):
            raise UnprocessableEntity(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)
    

    @field_validator("name", mode="before")
    def validate_name(cls, value) -> str:

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_NAME)
        
        return clean_string_field(value)
    

    @field_validator("birth_date", mode="before")
    def validate_birth_date(cls, value) -> str:
            
        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE)
        
        if not validate_date(value):

            raise UnprocessableEntity(ERROR_INVALID_FORMAT_BIRTH_DATE)
        
        if is_adult(value):

            raise UnprocessableEntity(ERROR_CHILD_INVALID_FIELD_BIRTH_DATE)
        
        return value


    @field_validator("gender", mode="before")
    def validate_gender(cls, value) -> str:

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_GENDER)
        
        if value not in Gender.__dict__.values():

            raise UnprocessableEntity(ERROR_INVALID_FORMAT_GENDER)
        
        return clean_string_field(value)
    

    @field_validator("class_id", mode="before")
    def validate_class_id(cls, value) -> str:

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_CLASS_ID)
        
        return clean_string_field(value)
    

    @field_validator("kinship", mode="before")
    def validate_kinship(cls, value) -> str:

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_KINSHIP)
        
        if value not in Kinship.__dict__.values():

            raise UnprocessableEntity(ERROR_CHILD_INVALID_FIELD_KINSHIP)
        
        return clean_string_field(value)
    
    @field_validator("parent_cpf", mode="before")
    def validate_parent_cpf(cls, value) -> str:

        value = value.strip()

        if not value:
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_PARENT_CPF)

        if not validate_cpf(value):
            raise UnprocessableEntity(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)

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
        examples=["20240000001", "20240000002"]
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


    @field_validator("shift", mode="before")
    def validate_shift(cls, value) -> str:

        if value not in Shift.__dict__.values():
            raise UnprocessableEntity(ERROR_INVALID_FORMAT_SHIFT)

        return clean_string_field(value)


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


    @field_validator("cpf", mode="before")
    def validate_cpf(cls, value) -> str:

        value = value.strip()

        if not value:
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_CPF)

        if not validate_cpf(value):
            raise UnprocessableEntity(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)
    

    @field_validator("name", mode="before")
    def validate_name(cls, value) -> str:

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_NAME)
        
        return clean_string_field(value)
    

    @field_validator("birth_date", mode="before")
    def validate_birth_date(cls, value) -> str:
            
        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE)
        
        if not validate_date(value):

            raise UnprocessableEntity(ERROR_INVALID_FORMAT_BIRTH_DATE)
        
        if is_adult(value):

            raise UnprocessableEntity(ERROR_CHILD_INVALID_FIELD_BIRTH_DATE)
        
        return value


    @field_validator("gender", mode="before")
    def validate_gender(cls, value) -> str:

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_CHILD_REQUIRED_FIELD_GENDER)
        
        if value not in Gender.__dict__.values():

            raise UnprocessableEntity(ERROR_INVALID_FORMAT_GENDER)
        
        return clean_string_field(value)