from fastapi import HTTPException
from pytest import raises


from constants.address import (
    ERROR_ADDRESS_REQUIRED_FIELD_STATE
)
from schemas.address import Address


def test_Address_Success():
    state = "PI"
    city = "Teresina"
    neighborhood = "Centro"
    street = "Rua A"
    house_number = "123"
    complement = "A"

    address = Address(
        state=state,
        city=city,
        neighborhood=neighborhood,
        street=street,
        house_number=house_number,
        complement=complement
    )

    assert address.state == state
    assert address.city == city
    assert address.neighborhood == neighborhood
    assert address.street == street
    assert address.house_number == house_number
    assert address.complement == complement

def test_Address_Success_no_complement():
    state = "PI"
    city = "Teresina"
    neighborhood = "Centro"
    street = "Rua A"
    house_number = "123"
    complement = ""

    address = Address(
        state=state,
        city=city,
        neighborhood=neighborhood,
        street=street,
        house_number=house_number,
        complement=complement
    )

    assert address.state == state
    assert address.city == city
    assert address.neighborhood == neighborhood
    assert address.street == street
    assert address.house_number == house_number
    assert address.complement == complement


def test_Address_Failed_state():
    state = ""
    city = "Teresina"
    neighborhood = "Centro"
    street = "Rua A"
    house_number = "123"
    complement = "A"

    with raises(HTTPException) as e:
        Address(
            state=state,
            city=city,
            neighborhood=neighborhood,
            street=street,
            house_number=house_number,
            complement=complement
        )

    e.value.detail == ERROR_ADDRESS_REQUIRED_FIELD_STATE
    e.value.status_code == 422