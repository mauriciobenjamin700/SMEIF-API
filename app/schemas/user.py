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
    validate_phone_number
)

class UserRequest(BaseSchema):
    """
    - cpf: str
    - name: str
    - phone: str
    - phone_optional: str
    - email: str
    - login: str
    - password: str
    - level: int
    """
    cpf: str = Field(title="cpf", description="CPF do usuário", examples=["123.456.789-00"])
    name: str = Field(title="name", description="Nome do usuário", examples=["John Doe"])
    phone: str = Field(title="phone", description="Telefone do usuário", examples=["(00) 00000-0000"])
    phone_optional: str = Field(title="phone_optional", description="Telefone opcional do usuário", examples=["(00) 00000-0000"])
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
    def field_validate_phone_optional(cls, values) -> str:
        value = values.get("phone_optional")
        if value:
            value = base_validation(value, "Telefone Opcional")

            phone = values.get("phone")

            if value == phone:
                raise HTTPException(400, "Telefone e Telefone Opcional não podem ser iguais")

            return validate_phone_number(value)
        
        return value
    
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
    def field_validate_level(cls, value) -> str:
        value =  base_validation(value, "Nível de Acesso")

        if value not in LEVEL.values():
            raise ValueError(f"Nível de Acesso inválido. Valores válidos: {', '.join(LEVEL.values())}")
        

