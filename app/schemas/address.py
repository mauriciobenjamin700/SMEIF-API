from pydantic import (
    Field,
    field_validator
)


from constants.address import(
    ERROR_ADDRESS_REQUIRED_FIELD_STATE,
    ERROR_ADDRESS_REQUIRED_FIELD_CITY,
    ERROR_ADDRESS_REQUIRED_FIELD_NEIGHBORHOOD,
    ERROR_ADDRESS_REQUIRED_FIELD_STREET,
    ERROR_ADDRESS_REQUIRED_FIELD_HOUSE_NUMBER
)
from schemas.base import BaseSchema
from utils.format import clean_string_field
from utils.messages.error import UnprocessableEntity


class AddressRequest(BaseSchema):
    """
    - state: str
    - city: str
    - neighborhood: str
    - street: str
    - house_number: str
    - complement: str = ""
    """
    state: str = Field(title="state", description="Estado", examples=["PI", "SP"])
    city: str = Field(title="city", description="Cidade", examples=["Teresina", "São Paulo"])
    neighborhood: str = Field(title="neighborhood", description="Bairro", examples=["Centro", "Vila"])
    street: str = Field(title="street", description="Rua", examples=["Rua A", "Rua B"])
    house_number: str = Field(title="house_number", description="Número da casa", examples=["123", "456"])
    complement: str = Field(title="complement", description="Complemento", examples=["A", "B"], default="")


    @field_validator("state", mode="before")
    def field_validate_state(cls, value) -> str:
        value = clean_string_field(value)

        if not value:
            raise UnprocessableEntity(ERROR_ADDRESS_REQUIRED_FIELD_STATE)

        return value
    

    @field_validator("city", mode="before")
    def field_validate_city(cls, value) -> str:
        value = clean_string_field(value)

        if not value:
            raise UnprocessableEntity(ERROR_ADDRESS_REQUIRED_FIELD_CITY)

        return value
    

    @field_validator("neighborhood", mode="before")
    def field_validate_neighborhood(cls, value) -> str:
        value = clean_string_field(value)

        if not value:
            raise UnprocessableEntity(ERROR_ADDRESS_REQUIRED_FIELD_NEIGHBORHOOD)
        
        return value
    

    @field_validator("street", mode="before")
    def field_validate_street(cls, value) -> str:
        value = clean_string_field(value)

        if not value:
            raise UnprocessableEntity(ERROR_ADDRESS_REQUIRED_FIELD_STREET)
        
        return value
    

    @field_validator("house_number", mode="before")
    def field_validate_house_number(cls, value) -> str:
        value = clean_string_field(value)
        
        if not value:
            raise UnprocessableEntity(ERROR_ADDRESS_REQUIRED_FIELD_HOUSE_NUMBER)
        
        return value