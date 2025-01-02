from fastapi import HTTPException
from pytest import raises


from constants.user import (
    ERROR_USER_NOT_FOUND_USER, 
    ERROR_USER_NOT_ID,
    ERROR_USER_REQUIRED_FIELD_CPF
)
from useCases.user import UserUseCases
from schemas.user import UserResponse
from utils.format import (
    format_cpf,
    format_phone,
    format_date
)

def test_get_user_success(db_session, mock_user_on_db):

    uc = UserUseCases(db_session)

    user = uc.get(mock_user_on_db.cpf)

    assert isinstance(user, UserResponse)
    assert user.cpf == format_cpf(mock_user_on_db.cpf)
    assert user.name == mock_user_on_db.name
    assert user.birth_date == format_date(mock_user_on_db.birth_date)
    assert user.gender == mock_user_on_db.gender
    assert user.phone == format_phone(mock_user_on_db.phone)
    assert user.phone_optional == ""
    assert user.email == mock_user_on_db.email
    assert user.level == mock_user_on_db.level
    assert user.state == mock_user_on_db.state
    assert user.city == mock_user_on_db.city
    assert user.neighborhood == mock_user_on_db.neighborhood
    assert user.street == mock_user_on_db.street
    assert user.house_number == mock_user_on_db.house_number


def test_get_user_fail_no_id(db_session):
    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.get("")

    assert e.value.status_code == 400
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_CPF


def test_get_user_fail_not_found(db_session):
    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.get("999.999.999-99")

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_USER_NOT_FOUND_USER