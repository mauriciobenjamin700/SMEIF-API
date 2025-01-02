from datetime import datetime
from pydantic import (
    Field,
    field_validator,
    model_validator
)


from constants.base import (
    ERROR_INVALID_CPF, 
    ERROR_INVALID_EMAIL,
    ERROR_INVALID_FORMAT_BIRTH_DATE,
    ERROR_INVALID_FORMAT_GENDER, 
    ERROR_INVALID_PHONE, 
    ERROR_INVALID_PHONE_OPTIONAL
)
from constants.user import (
    ERROR_USER_INVALID_BIRTHDATE,
    ERROR_USER_INVALID_LEVEL,
    ERROR_USER_PHONE_AND_OPTIONAL_PHONE_EQUALS,
    ERROR_USER_REQUIRED_FIELD_ADDRESS,
    ERROR_USER_REQUIRED_FIELD_BIRTH_DATE,
    ERROR_USER_REQUIRED_FIELD_CPF,
    ERROR_USER_REQUIRED_FIELD_EMAIL,
    ERROR_USER_REQUIRED_FIELD_GENDER,
    ERROR_USER_REQUIRED_FIELD_NAME,
    ERROR_USER_REQUIRED_FIELD_PASSWORD,
    ERROR_USER_REQUIRED_FIELD_PHONE
)
from schemas.address import Address
from schemas.base import (
    BaseSchema,
    Gender,
    UserLevel
)
from utils.validate import(
    is_adult,
    validate_cpf,
    validate_date,
    validate_email,
    validate_phone_number,
    validate_string
)
from utils.format import (
    clean_string_field,
    format_cpf,
    format_date,
    format_phone,
    unformat_cpf,
    unformat_phone
)
from utils.messages.error import UnprocessableEntity


class UserRequest(BaseSchema):
    """
    - cpf: str
    - name: str
    - birth_date: str
    - gender: str
    - phone: str
    - phone_optional: str = ""
    - email: str
    - password: str
    - level: int
    - address: Address
    """
    cpf: str = Field(
        title="cpf", 
        description="CPF do usuário", 
        examples=["123.456.789-00"]
    )
    name: str = Field(
        title="name", 
        description="Nome do usuário", 
        examples=["John Doe"]
    )
    birth_date: str = Field(
        title="birth_date", 
        description="Data de nascimento do usuário", 
        examples=["2000-12-25"]
    )
    gender: Gender = Field(
        title="gender", 
        description="Gênero do usuário", 
        examples=["M", "F","Z"]
    )
    phone: str = Field(
        title="phone", 
        description="Telefone do usuário", 
        examples=["(00) 90000-0000"]
    )
    phone_optional: str = Field(
        title="phone_optional", 
        description="Telefone opcional do usuário", 
        examples=["(00) 90000-0001"], default=""
    )
    email: str = Field(
        title="email", 
        description="E-mail do usuário", 
        examples=["test@example.com"]
    )
    password: str = Field(
        title="password", 
        description="Senha do usuário", 
        examples=["123456"]
    )
    level: UserLevel = Field(
        title="level", 
        description="Nível de acesso do usuário", 
        examples=[
            UserLevel.PARENT.value,
            UserLevel.TEACHER.value,
            UserLevel.COORDINATION.value,
            UserLevel.ADMIN.value
        ]
    )
    address: Address = Field(
        title="address", 
        description="Endereço do usuário"
    )


    @field_validator("cpf", mode="before")
    def field_validate_cpf(cls, value) -> str:
        
        if not validate_string(value):

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_CPF)

        if not validate_cpf(value):

            raise UnprocessableEntity(ERROR_INVALID_CPF)
        
        return unformat_cpf(value)
    
    @field_validator("name", mode="before")
    def field_validate_name(cls, value) -> str:
        
        if not validate_string(value):

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_NAME)
        
        return value
    

    @field_validator("birth_date", mode="before")
    def field_validate_birth_date(cls, value) -> str:
        
        if not validate_string(value):

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_BIRTH_DATE)
        
        if not validate_date(value):

            raise UnprocessableEntity(ERROR_INVALID_FORMAT_BIRTH_DATE)
        
        if not is_adult(value):

            raise UnprocessableEntity(ERROR_USER_INVALID_BIRTHDATE)
        
        return value
    

    @field_validator("gender", mode="before")
    def field_validate_gender(cls, value) -> str:
        
        if not validate_string(value):

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_GENDER)
        
        if value not in Gender.__dict__.values():

            raise UnprocessableEntity(ERROR_INVALID_FORMAT_GENDER)
        
        return value
    
    @field_validator("phone", mode="before")
    def field_validate_phone(cls, value) -> str:

        if not validate_string(value):

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_PHONE)
        
        if not validate_phone_number(value):

            raise UnprocessableEntity(ERROR_INVALID_PHONE)
        
        return unformat_phone(value)
    
    @model_validator(mode="before")
    def field_validate_phone_optional(cls, values) -> dict:

        value = values.get("phone_optional")

        if validate_string(value):

            if not validate_phone_number(value):

                raise UnprocessableEntity(ERROR_INVALID_PHONE_OPTIONAL)


            phone = values.get("phone")

            if not validate_string(phone):

                raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_PHONE)

            if value == phone:

                raise UnprocessableEntity(ERROR_USER_PHONE_AND_OPTIONAL_PHONE_EQUALS)
            
            if not validate_phone_number(value):

                raise UnprocessableEntity(ERROR_INVALID_PHONE_OPTIONAL)

            values["phone_optional"] = unformat_phone(value)
        
        else:
            values["phone_optional"] = ""
        
        return values
    
    @field_validator("email", mode="before")
    def field_validate_email(cls, value) -> str:
        
        if not validate_string(value):

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_EMAIL)
        
        if not validate_email(value):

            raise UnprocessableEntity(ERROR_INVALID_EMAIL)
        
        return value
    
    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:
        
        if not validate_string(value):

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_PASSWORD)
        
        return value
    
    @field_validator("level", mode="before")
    def field_validate_level(cls, value) -> int:

        if not value or value not in UserLevel.__dict__.values():

            raise UnprocessableEntity(ERROR_USER_INVALID_LEVEL)
        
        return value
    
    @field_validator("address", mode="before")
    def field_validate_address(cls, value) -> Address:
            
            if not value:
    
                raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_ADDRESS)
            
            return value


class UserDB(BaseSchema):
    """
    - cpf: str
    - name: str
    - birth_date: datetime
    - gender: str
    - phone: str
    - phone_optional: str | None
    - email: str
    - password: str
    - level: int
    - state: str
    - city: str
    - neighborhood: str
    - street: str
    - house_number: str
    - complement: str | None
    """

    cpf: str
    name: str
    birth_date: datetime
    gender: str
    phone: str
    phone_optional: str | None
    email: str
    password: str
    level: int
    state: str
    city: str
    neighborhood: str
    street: str
    house_number: str
    complement: str | None

    @field_validator("phone_optional", mode="before")
    def field_validate_phone_optional(cls, value) -> str:
        if not value:
            value = None

        return value
    
    @field_validator("complement", mode="before")
    def field_validate_complement(cls, value) -> str:
        if not value:
            value = None
    
        return value
        
class UserResponse(BaseSchema):
    """
    - cpf: str
    - name: str
    - birth_date: str
    - gender: str [M, F , Z]
    - phone: str
    - phone_optional: str = ""
    - email: str
    - level: int
    - state: str
    - city: str
    - neighborhood: str
    - street: str
    - house_number: str
    - complement: str = ""
    """

    cpf: str = Field(
        title="cpf", 
        description="CPF do usuário", 
        examples=["123.456.789-00"]
    )
    name: str = Field(
        title="name", 
        description="Nome do usuário", 
        examples=["John Doe"]
    )
    birth_date: str = Field(
        title="birth_date", 
        description="Data de nascimento do usuário", 
        examples=["01/01/2000"]
    )
    gender: Gender = Field(
        title="gender", 
        description="Gênero do usuário", 
        examples=["Masculino", "Feminino","Outros"]
    )
    phone: str = Field(
        title="phone", 
        description="Telefone do usuário", 
        examples=["(00) 90000-0000"]
    )
    phone_optional: str = Field(
        title="phone_optional", 
        description="Telefone opcional do usuário", 
        examples=["(00) 00000-0000"], default=""
    )
    email: str = Field(
        title="email", 
        description="E-mail do usuário", 
        examples=["jhon.doe@gmail.com"]
    )
    level: UserLevel = Field(
        title="level", 
        description="Nível de acesso do usuário", 
        examples=["1"]
    )
    state: str = Field(
        title="state", 
        description="Estado do usuário", 
        examples=["SP"]
    )
    city: str = Field(
        title="city", 
        description="Cidade do usuário", 
        examples=["São Paulo"]
    )
    neighborhood: str = Field(
        title="neighborhood", 
        description="Bairro do usuário", 
        examples=["Vila Maria"]
    )
    street: str = Field(
        title="street", 
        description="Rua do usuário", 
        examples=["Rua dos Bandeirantes"]
    )
    house_number: str = Field(
        title="house_number", 
        description="Número da casa do usuário", 
        examples=["100"]
    )
    complement: str = Field(
        title="complement", 
        description="Complemento do endereço do usuário", 
        examples=["Apartamento 201"]
    )

    @field_validator("cpf", mode="before")
    def field_validate_cpf(cls, value) -> str:
        
        value = clean_string_field(value)
        value = unformat_cpf(value)
        value  = format_cpf(value)

        return value
    

    @field_validator("phone", mode="before")
    def field_validate_phone(cls, value) -> str:
        value = clean_string_field(value)
        value = unformat_phone(value)
        value = format_phone(value)
        return value


    @field_validator("phone_optional", mode="before")
    def field_validate_phone_optional(cls, value) -> str:
        if not value:
            value = ""

        else:
            value = clean_string_field(value)
            value = unformat_phone(value)
            value = format_phone(value)

        return value

    @field_validator("complement", mode="before")
    def field_validate_complement(cls, value) -> str:
        if not value:
            value = ""
        return value
    
    @field_validator("birth_date", mode="before")
    def field_validate_birth_date(cls, value) -> str:
        if isinstance(value, datetime):
            value = format_date(value)
        
        return value

class UserUpdateRequest(BaseSchema):
    """
    - name: str | None
    - phone: str | None
    - phone_optional: str | None
    - email: str | None
    - password: str | None
    - level: int | None
    - address: Address | None
    """
    name: str | None = Field(
        title="name", 
        description="Nome do usuário", 
        examples=["John Doe"], 
        default=None
    )
    phone: str | None = Field(
        title="phone", 
        description="Telefone do usuário", 
        examples=["(00) 90000-0000"], 
        default=None
    )
    phone_optional: str | None = Field(
        title="phone_optional", 
        description="Telefone opcional do usuário", 
        examples=["(00) 9000-0000"], 
        default=None
    )
    email: str |  None = Field(
        title="email", 
        description="E-mail do usuário", 
        examples=["jhon.doe@gmail.com"], 
        default=None
    )
    password: str | None = Field(
        title="password", 
        description="Senha do usuário", 
        examples=["123456"], 
        default=None
    )
    level: UserLevel | None = Field(
        title="level", 
        description="Nível de acesso do usuário", 
        examples=[1,2], 
        default=None
    )
    address: Address | None = Field(
        title="address", 
        description="Endereço do usuário", 
        default=None
    )

    @field_validator("name", mode="before")
    def field_validate_name(cls, value) -> str:
        value =  clean_string_field(value)

        return value
    
    @field_validator("phone", mode="before")
    def field_validate_phone(cls, value) -> str:

        value = clean_string_field(value)

        if value:

            if not validate_phone_number(value):

                raise UnprocessableEntity(ERROR_INVALID_PHONE)

            value = unformat_phone(value)

        return value
    

    @field_validator("phone_optional", mode="before")
    def field_validate_phone_optional(cls, value) -> str:

        value = clean_string_field(value)

        if value:

            if not validate_phone_number(value):

                raise UnprocessableEntity(ERROR_INVALID_PHONE_OPTIONAL)

            value = unformat_phone(value)

        return value
    
    @field_validator("email", mode="before")
    def field_validate_email(cls, value) -> str:

        value = clean_string_field(value)

        if value:

            if not validate_email(value):

                raise UnprocessableEntity(ERROR_INVALID_EMAIL)

            
        return value
    
    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:

        value = clean_string_field(value)

        return value


    @field_validator("level", mode="before")
    def field_validate_level(cls, value) -> int:

        if value:

            if value not in UserLevel.__dict__.values():

                raise UnprocessableEntity(ERROR_USER_INVALID_LEVEL)
        
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

        value =  clean_string_field(value)

        if not value:

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_CPF)
        
        if not validate_cpf(value):

            raise UnprocessableEntity(ERROR_INVALID_CPF)

        value = unformat_cpf(value)
        
        return value
    
    @field_validator("password", mode="before")
    def field_validate_password(cls, value) -> str:

        value =  clean_string_field(value)


        if not value:

            raise UnprocessableEntity(ERROR_USER_REQUIRED_FIELD_PASSWORD)
        
        return value
    

class AccessToken(BaseSchema):
    """
    - token: str
    """
    token: str = Field(
        title="token", 
        description="Token de acesso", 
        examples=["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyMzQ1.eyJzdWIiOiIyMzQ1"]
    )