from fastapi import HTTPException
from pytest import raises


from constants.user import (
    MESSAGE_ADD_SUCCESS,
    ERROR_CPF_ALREADY_EXISTS,
    ERROR_EMAIL_ALREADY_EXISTS,
    ERROR_PHONE_ALREADY_EXISTS
)
from controllers.user import UserUseCases
from database.models import UserModel
from schemas.user import UserRequest
from app.utils.security.cryptography import verify

def test_add_user_success(db_session, mock_UserRequest):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_UserRequest.dict())

    response = uc.add(user)

    assert response.detail == MESSAGE_ADD_SUCCESS

    user_in_db = db_session.query(UserModel).filter(UserModel.cpf == user.cpf).first()

    assert user_in_db.cpf == user.cpf
    assert user_in_db.name == user.name
    assert user_in_db.phone == user.phone
    assert user_in_db.phone_optional == user.phone_optional
    assert user_in_db.email == user.email
    assert verify(mock_UserRequest.password, user_in_db.password)
    assert user_in_db.level == user.level


def test_add_user_fail_cpf_exits(db_session, mock_user_on_db):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_user_on_db.dict())

    with raises(HTTPException) as e:
        uc.add(user)

    assert e.value.status_code == 409
    assert e.value.detail == ERROR_CPF_ALREADY_EXISTS


def test_add_user_fail_phone_exits(db_session, mock_UserRequest):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_UserRequest.dict())

    response = uc.add(user)

    assert response.detail == MESSAGE_ADD_SUCCESS

    user_in_db = db_session.query(UserModel).filter(UserModel.cpf == user.cpf).first()

    assert user_in_db.cpf == user.cpf
    assert user_in_db.name == user.name
    assert user_in_db.phone == user.phone
    assert user_in_db.phone_optional == user.phone_optional
    assert user_in_db.email == user.email
    assert verify(mock_UserRequest.password, user_in_db.password)
    assert user_in_db.level == user.level

    user.cpf = "321.321.321-21"

    with raises(HTTPException) as e:
        uc.add(user)

    assert e.value.status_code == 409
    assert e.value.detail == ERROR_PHONE_ALREADY_EXISTS


def test_add_user_fail_email_exits(db_session, mock_UserRequest):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_UserRequest.dict())

    response = uc.add(user)

    assert response.detail == MESSAGE_ADD_SUCCESS

    user_in_db = db_session.query(UserModel).filter(UserModel.cpf == user.cpf).first()

    assert user_in_db.cpf == user.cpf
    assert user_in_db.name == user.name
    assert user_in_db.phone == user.phone
    assert user_in_db.phone_optional == user.phone_optional
    assert user_in_db.email == user.email
    assert verify(mock_UserRequest.password, user_in_db.password)
    assert user_in_db.level == user.level

    user.cpf = "321.321.321-21"
    user.phone = "(99) 99999-9999"

    with raises(HTTPException) as e:
        uc.add(user)

    assert e.value.status_code == 409
    assert e.value.detail == ERROR_EMAIL_ALREADY_EXISTS