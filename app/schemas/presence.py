from datetime import (
    UTC, 
    datetime
)
from pydantic import (
    Field,
    field_validator
)


from constants.presence import(
    ERROR_PRESENCE_INVALID_FIELD_TYPE,
    ERROR_PRESENCE_REQUIRED_FIELD_CLASS_EVENT_ID,
    ERROR_PRESENCE_REQUIRED_FIELD_TYPE
)
from schemas.base import (
    BaseSchema,
    PresenceType
)
from services.generator.ids import id_generate
from utils.format import clean_string_field
from utils.messages.error import UnprocessableEntity
from utils.validate import (
    validate_string,
    validate_and_format_child_cpf
)


class PresenceRequest(BaseSchema):
    """
    - class_event_id: str: ID da Aula
    - child_cpf: str: CPF da criança
    - type: PresenceType: Tipo de presença (P: presente, F: faltou)
    """
    class_event_id: str = Field(
        title="ID da Aula",
        description="ID da Aula que o aluno está presente ou ausente",
        examples=["123456"],
        default=None,
        validate_default=True
    )
    child_cpf: str = Field(
        title="CPF da criança",
        description="CPF da criança que está presente ou ausente",
        examples=["123.456.789-01"],
        default=None,
        validate_default=True
    )
    type: PresenceType = Field(
        title="Tipo de presença",
        description="Tipo de presença (P: presente, F: faltou)",
        examples=[PresenceType.P.value, PresenceType.F.value],
        default=None,
        validate_default=True
    )

    
    @field_validator("class_event_id", mode="before")
    def validate_class_event_id(cls, value) -> str:
        
        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_PRESENCE_REQUIRED_FIELD_CLASS_EVENT_ID)

        return value


    @field_validator("child_cpf", mode="before")
    def validate_child_cpf(cls, value) -> str:

        value = clean_string_field(value)

        value = validate_and_format_child_cpf(value)

        return value


    @field_validator("type", mode="before")
    def validate_type(cls, value) -> str:

        value = clean_string_field(value)

        if not validate_string(value):
            raise UnprocessableEntity(ERROR_PRESENCE_REQUIRED_FIELD_TYPE)

        if value not in [PresenceType.P.value, PresenceType.F.value]:
            raise UnprocessableEntity(ERROR_PRESENCE_INVALID_FIELD_TYPE)

        return value

class PresenceDB(PresenceRequest):
    """
    - id: str: ID da presença
    - created_at: datetime: Data e hora da criação da presença
    - class_event_id: str: ID da Aula
    - child_cpf: str: CPF da criança
    - type: PresenceType: Tipo de presença (P: presente, F: faltou)

    """
    id: str = Field(
        title="ID",
        description="ID da presença",
        examples=["123456"],
        default_factory=id_generate,
        frozen=True
    )
    created_at: datetime = Field(
        title="Data e hora da criação",
        description="Data e hora da criação da presença",
        examples=[datetime.now(tz=UTC)],
        default_factory=datetime.now,
        frozen=True
    )


class PresenceResponse(BaseSchema):
    """
    - id: str: ID da presença
    - created_at: str: Data e hora da criação da presença
    - class_event_id: str: ID da Aula
    - child_cpf: str: CPF da criança
    - type: PresenceType: Tipo de presença (P: presente, F: faltou)
    - date: str: Data da aula
    - duration: str: Duração da aula
    - class_info: str: EX: "5° ano A"
    """
    id: str = Field(
        title="ID",
        description="ID da presença",
        examples=["123456"]
    )
    created_at: str = Field(
        title="Data e hora da criação",
        description="Data e hora da criação da presença",
        examples=["2030-12-10"]
    )
    class_event_id: str = Field(
        title="ID da Aula",
        description="ID da Aula que o aluno está presente ou ausente",
        examples=["123456"]
    )
    child_cpf: str = Field(
        title="CPF da criança",
        description="CPF da criança que está presente ou ausente",
        examples=["123.456.789-01"]
    )
    type: PresenceType = Field(
        title="Tipo de presença",
        description="Tipo de presença (P: presente, F: faltou)",
        examples=[PresenceType.P.value, PresenceType.F.value]
    )
    date: str = Field(
        title="Data da aula",
        description="Data de início da aula",
        examples=["10-12-2030"]
    )
    duration: str = Field(
        title="Horário de término da aula",
        description="Hora que a aula começa e deve terminar da aula",
        examples=["08:00 - 10:00", "14:00 - 16:00"]
    )
    class_info: str = Field(
        title="Informações da aula",
        description="Informações da aula",
        examples=["5° ano A", "6° ano B", "8° ano C"]
    )


    @field_validator("child_cpf", mode="before")
    def validate_child_cpf(cls, value) -> str:

        value = validate_and_format_child_cpf(value)

        return value