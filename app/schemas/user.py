"""
- DataClasses for User
    - UserRequest
    - UserResponse
    - UserUpdateRequest
    - UserLoginRequest
"""

from fastapi import HTTPException
from pydantic import (
    Field,
    field_validator,
    model_validator
)


from constants.user import LEVEL
from schemas.base import BaseSchema
from utils.validate import(
    base_validation,
    validate_cpf,
    validate_email,
    validate_phone_number,
    validate_string_field
)

class UserRequest(BaseSchema):
    """
    - cpf: str
    - name: str
    - phone: str
    - phone_optional: str = "
    - email: str
    - login: str
    - password: str
    - level: int
    """
    cpf: str = Field(title="cpf", description="CPF do usuário", examples=["123.456.789-00"])
    name: str = Field(title="name", description="Nome do usuário", examples=["John Doe"])
    phone: str = Field(title="phone", description="Telefone do usuário", examples=["(00) 90000-0000"])
    phone_optional: str = Field(title="phone_optional", description="Telefone opcional do usuário", examples=["(00) 9000-0000"], default="")
    email: str = Field(title="email", description="E-mail do usuário", examples=["test@example.com"])
    login: str = Field(title="login", description="Login do usuário", examples=["john.doe"])
    password: str = Field(title="password", description="Senha do usuário", examples=["123456"])
    level: int = Field(title="level", description="Nível de acesso do usuário", examples=[f"{key}: {value}" for key, value in LEVEL.items()])


    @field_validator("cpf", mode="before")
    def field_validate_cpf(cls, value) -> str:
        value = base_validation(value, "CPF")
        return validate_cpf(value)
    
    @field_validator("name", mode="before")
    def field_validate_name(cls, value) -> str:
        return base_validation(value, "Nome")
    
    @field_validator("phone", mode="before")
    def field_validate_phone(cls, value) -> str:
        value = base_validation(value, "Telefone")
        return validate_phone_number(value)
    
    @model_validator(mode="before")
    def field_validate_phone_optional(cls, values) -> dict:
        value = values.get("phone_optional")
        if value and value.strip() != "":
            value = base_validation(value, "Telefone Opcional")

            phone = values.get("phone")

            if value == phone:
                raise HTTPException(400, "Telefone e Telefone Opcional não podem ser iguais")

            values["phone_optional"] = validate_phone_number(value)
        
        else:
            values["phone_optional"] = ""
        
        return values
    
    @field_validator("email", mode="before")
    def field_validate_email(cls, value) -> str:
        value = base_validation(value, "E-mail")
        return validate_email(value)
    
    @field_validator("login", mode="before")
    def field_validate_login(cls, value) -> str:
        return base_validation(value, "Login")
    
    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:
        return base_validation(value, "Senha")
    
    @field_validator("level", mode="before")
    def field_validate_level(cls, value) -> int:

        if not value or value not in LEVEL.values():
            raise HTTPException(400,"Nível de Acesso inválido")
        
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
    name: str = Field(title="name", description="Nome do usuário", examples=["John Doe"], default=None)
    phone: str = Field(title="phone", description="Telefone do usuário", examples=["(00) 90000-0000"], default=None)
    phone_optional: str = Field(title="phone_optional", description="Telefone opcional do usuário", examples=["(00) 9000-0000"], default=None)
    email: str = Field(title="email", description="E-mail do usuário", examples=["jhon.doe@gmail.com"], default=None)
    login: str = Field(title="login", description="Login do usuário", examples=["john.doe"], default=None)
    password: str = Field(title="password", description="Senha do usuário", examples=["123456"], default=None)
    level: int = Field(title="level", description="Nível de acesso do usuário", examples=["2"], default=None)

    @field_validator("name", mode="before")
    def field_validate_name(cls, value) -> str:
        return validate_string_field(value)
    
    @field_validator("phone", mode="before")
    def field_validate_phone(cls, value) -> str:

        if validate_string_field(value):

            value = validate_phone_number(value)

        return value
    

    @field_validator("phone_optional", mode="before")
    def field_validate_phone(cls, value) -> str:

        if validate_string_field(value):
            
            value = validate_phone_number(value)

        return value
    
    @field_validator("email", mode="before")
    def field_validate_email(cls, value) -> str:

        if validate_string_field(value):

            value =  validate_email(value)
            
        return value
    
    @field_validator("login", mode="before")
    def field_validate_login(cls, value) -> str:

        return validate_string_field(value)
    

    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:

        return validate_string_field(value)


    @field_validator("level", mode="before")
    def field_validate_level(cls, value) -> int:
        if value:
            if value not in LEVEL.values():
                raise HTTPException(400,"Nível de Acesso inválido")
        
        return value


class UserLoginRequest(BaseSchema):
    """
    - login: str
    - password: str
    """
    login: str = Field(title="login", description="Login do usuário", examples=["john.doe"])
    password: str = Field(title="password", description="Senha do usuário", examples=["123456"])

    @field_validator("login", mode="before")
    def field_validate_login(cls, value) -> str:

        value =  validate_string_field(value)

        if not value:

            raise HTTPException(400, "Login não informado")
        
        return value
    
    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:

        value =  validate_string_field(value)

        if not value:

            raise HTTPException(400, "Senha não informada")
        
        return value