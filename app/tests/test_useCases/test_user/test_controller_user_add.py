from fastapi import HTTPException
from pytest import raises


from constants.user import (
    MESSAGE_USER_ADD_SUCCESS,
    ERROR_USER_CPF_ALREADY_EXISTS,
    ERROR_USER_EMAIL_ALREADY_EXISTS,
    ERROR_USER_PHONE_ALREADY_EXISTS
)
from useCases.user import UserUseCases
from database.models import UserModel
from schemas.user import UserRequest
from services.security.password import verify
from utils.format import(
    format_date,
    format_phone,
    format_string_date
)

def test_add_user_success(db_session, mock_UserRequest):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_UserRequest.dict())

    response = uc.add(user)

    assert response.detail == MESSAGE_USER_ADD_SUCCESS

    user_in_db = db_session.query(UserModel).filter(UserModel.cpf == user.cpf).first()

    assert user_in_db.cpf == user.cpf
    assert user_in_db.name == user.name
    assert format_date(user_in_db.birth_date) == format_string_date(user.birth_date)
    assert user_in_db.gender == user.gender
    assert user_in_db.phone == user.phone
    assert user_in_db.phone_optional == None
    assert user_in_db.email == user.email
    assert verify(mock_UserRequest.password, user_in_db.password)
    assert user_in_db.level == user.level
    assert user_in_db.state == user.address.state
    assert user_in_db.city == user.address.city
    assert user_in_db.neighborhood == user.address.neighborhood
    assert user_in_db.street == user.address.street
    assert user_in_db.house_number == user.address.house_number
    assert user_in_db.complement == user.address.complement


def test_add_user_fail_cpf_exits(db_session, mock_UserRequest):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_UserRequest.dict())

    with raises(HTTPException) as e:
        uc.add(user)
        uc.add(user)

    assert e.value.status_code == 409
    assert e.value.detail == ERROR_USER_CPF_ALREADY_EXISTS


def test_add_user_fail_phone_exits(db_session, mock_UserRequest):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_UserRequest.dict())

    _ = uc.add(user)

    user.cpf = "321.321.321-21"

    with raises(HTTPException) as e:
        uc.add(user)

    assert e.value.status_code == 409
    assert e.value.detail == ERROR_USER_PHONE_ALREADY_EXISTS


def test_add_user_fail_email_exits(db_session, mock_UserRequest):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_UserRequest.dict())

    _ = uc.add(user)


    user.cpf = "321.321.321-21"
    user.phone = "(99) 99999-9999"

    with raises(HTTPException) as e:
        uc.add(user)

    assert e.value.status_code == 409
    assert e.value.detail == ERROR_USER_EMAIL_ALREADY_EXISTS