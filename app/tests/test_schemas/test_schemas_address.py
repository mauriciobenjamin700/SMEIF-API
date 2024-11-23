from fastapi import HTTPException
from pytest import raises


from constants.address import (
    ERROR_ADDRESS_REQUIRED_FIELD_STATE
)
from schemas.address import AddressRequest


def test_AddressRequest_Success():
    state = "PI"
    city = "Teresina"
    neighborhood = "Centro"
    street = "Rua A"
    house_number = "123"
    complement = "A"

    address = AddressRequest(
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

def test_AddressRequest_Success_no_complement():
    state = "PI"
    city = "Teresina"
    neighborhood = "Centro"
    street = "Rua A"
    house_number = "123"
    complement = ""

    address = AddressRequest(
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


def test_AddressRequest_Failed_state():
    state = ""
    city = "Teresina"
    neighborhood = "Centro"
    street = "Rua A"
    house_number = "123"
    complement = "A"

    with raises(HTTPException) as e:
        AddressRequest(
            state=state,
            city=city,
            neighborhood=neighborhood,
            street=street,
            house_number=house_number,
            complement=complement
        )

    e.value.detail == ERROR_ADDRESS_REQUIRED_FIELD_STATE
    e.value.status_code == 422