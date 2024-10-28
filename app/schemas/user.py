"""
- DataClasses for User
    - UserRequest
    - UserResponse
    - UserUpdateRequest
    - UserLoginRequest
"""
from pydantic import (
    Field,
    field_validator,
    model_validator
)


from constants.base import ERROR_INVALID_CPF, ERROR_INVALID_PHONE, ERROR_INVALID_PHONE_OPTIONAL
from constants.user import (
    ERROR_PHONE_AND_OPTIONAL_PHONE_EQUALS,
    ERROR_USER_REQUIRED_FIELD_CPF,
    ERROR_USER_REQUIRED_FIELD_NAME,
    ERROR_USER_REQUIRED_FIELD_PHONE, 
    LEVEL
)
from schemas.base import BaseSchema
from utils.validate import(
    base_validation,
    validate_cpf,
    validate_email,
    validate_phone_number,
    validate_string
)
from utils.format import (
    unformat_cpf,
    unformat_phone
)
from utils.messages import ValidationErrorMessage



class UserRequest(BaseSchema):
    """
    - cpf: str
    - name: str
    - phone: str
    - phone_optional: str = ""
    - email: str
    - password: str
    - level: int
    """
    cpf: str = Field(title="cpf", description="CPF do usuário", examples=["123.456.789-00"])
    name: str = Field(title="name", description="Nome do usuário", examples=["John Doe"])
    phone: str = Field(title="phone", description="Telefone do usuário", examples=["(00) 90000-0000"])
    phone_optional: str = Field(title="phone_optional", description="Telefone opcional do usuário", examples=["(00) 9000-0000"], default="")
    email: str = Field(title="email", description="E-mail do usuário", examples=["test@example.com"])
    password: str = Field(title="password", description="Senha do usuário", examples=["123456"])
    level: int = Field(title="level", description="Nível de acesso do usuário", examples=[f"{key}: {value}" for key, value in LEVEL.items()])


    @field_validator("cpf", mode="before")
    def field_validate_cpf(cls, value) -> str:
        
        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_USER_REQUIRED_FIELD_CPF)

        if not validate_cpf(value):

            raise ValidationErrorMessage(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)
    
    @field_validator("name", mode="before")
    def field_validate_name(cls, value) -> str:
        
        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_USER_REQUIRED_FIELD_NAME)
        
        return value
    
    @field_validator("phone", mode="before")
    def field_validate_phone(cls, value) -> str:

        if not validate_string(value):

            raise ValidationErrorMessage(ERROR_USER_REQUIRED_FIELD_PHONE)
        
        if not validate_phone_number(value):

            raise ValidationErrorMessage(ERROR_INVALID_PHONE)
        
        return unformat_phone(value)
    
    @model_validator(mode="before")
    def field_validate_phone_optional(cls, values) -> dict:

        value = values.get("phone_optional")

        if validate_string(value):

            value = base_validation(value, "Telefone Opcional")

            phone = values.get("phone")

            if value == phone:
                raise ValidationErrorMessage(ERROR_PHONE_AND_OPTIONAL_PHONE_EQUALS)
            
            if not validate_phone_number(value):

                raise ValidationErrorMessage(ERROR_INVALID_PHONE_OPTIONAL)

            values["phone_optional"] = validate_phone_number(value)
        
        else:
            values["phone_optional"] = ""
        
        return values
    
    @field_validator("email", mode="before")
    def field_validate_email(cls, value) -> str:
        value = base_validation(value, "E-mail")
        return validate_email(value)
    
    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:
        return base_validation(value, "Senha")
    
    @field_validator("level", mode="before")
    def field_validate_level(cls, value) -> int:

        if not value or value not in LEVEL.values():
            raise ErrorMessage(400,"Nível de Acesso inválido")
        
        return value
        
class UserResponse(BaseSchema):
    """
    - cpf: str
    - name: str
    - phone: str
    - phone_optional: str = ""
    - email: str
    - level: int
    """

    cpf: str = Field(title="cpf", description="CPF do usuário", examples=["123.456.789-00"])
    name: str = Field(title="name", description="Nome do usuário", examples=["John Doe"])
    phone: str = Field(title="phone", description="Telefone do usuário", examples=["(00) 90000-0000"])
    phone_optional: str = Field(title="phone_optional", description="Telefone opcional do usuário", examples=["(00) 00000-0000"], default="")
    email: str = Field(title="email", description="E-mail do usuário", examples=["jhon.doe@gmail.com"])
    level: int = Field(title="level", description="Nível de acesso do usuário", examples=["1"])

    @field_validator("phone_optional", mode="before")
    def field_validate_phone_optional(cls, value) -> str:
        if not value:
            value = ""

        return value

class UserUpdateRequest(BaseSchema):
    """
    - name: str | None
    - phone: str | None
    - phone_optional: str | None
    - email: str | None
    - password: str | None
    """
    name: str | None = Field(title="name", description="Nome do usuário", examples=["John Doe"], default=None)
    phone: str | None = Field(title="phone", description="Telefone do usuário", examples=["(00) 90000-0000"], default=None)
    phone_optional: str | None = Field(title="phone_optional", description="Telefone opcional do usuário", examples=["(00) 9000-0000"], default=None)
    email: str |  None = Field(title="email", description="E-mail do usuário", examples=["jhon.doe@gmail.com"], default=None)
    password: str = Field(title="password", description="Senha do usuário", examples=["123456"], default=None)
    level: int = Field(title="level", description="Nível de acesso do usuário", examples=["2"], default=None)

    @field_validator("name", mode="before")
    def field_validate_name(cls, value) -> str:
        value =  validate_string_field(value)

        return value
    
    @field_validator("phone", mode="before")
    def field_validate_phone(cls, value) -> str:

        if validate_string_field(value):

            value = validate_phone_number(value)

        return value
    

    @field_validator("phone_optional", mode="before")
    def field_validate_phone_optional(cls, value) -> str:

        if validate_string_field(value):
            
            value = validate_phone_number(value)


        return value
    
    @field_validator("email", mode="before")
    def field_validate_email(cls, value) -> str:

        if validate_string_field(value):

            value =  validate_email(value)
            
        return value
    
    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:

        return validate_string_field(value)


    @field_validator("level", mode="before")
    def field_validate_level(cls, value) -> int:
        if value:
            if value not in LEVEL.values():
                raise ErrorMessage(400,"Nível de Acesso inválido")
        
        return value


class UserLoginRequest(BaseSchema):
    """
    - cpf: str
    - password: str
    """
    cpf: str = Field(title="CPF", description="CPF do usuário", examples=["123.123.123.12"])
    password: str = Field(title="password", description="Senha do usuário", examples=["123456"])

    @field_validator("cpf", mode="before")
    def field_validate_login(cls, value) -> str:

        value =  validate_string_field(value)

        if not value:

            raise ErrorMessage(400, "CPF não informado")
        
        value = validate_cpf(value)
        
        return value
    
    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:

        value =  validate_string_field(value)

        if not value:

            raise ErrorMessage(400, "Senha não informada")
        
        return value