from fastapi import HTTPException
from pytest import raises


from constants.user import (
    ERROR_USER_NOT_FOUND_USER,
    ERROR_USER_PASSWORD_WRONG
)
from controllers.user import UserUseCases
from schemas.user import UserLoginRequest, UserResponse
from app.services.security.tokens import decode_token


def test_login_user_sucess(db_session, mock_user_on_db, mock_UserLoginRequest):

    uc = UserUseCases(db_session)

    response = uc.login(mock_UserLoginRequest)

    assert isinstance(response, str)

    data = decode_token(response)

    user = UserResponse(**data)

    assert user.cpf == mock_user_on_db.cpf
    assert user.name == mock_user_on_db.name
    assert user.phone == mock_user_on_db.phone
    assert user.phone_optional == mock_user_on_db.phone_optional
    assert user.email == mock_user_on_db.email
    assert user.level == mock_user_on_db.level


def test_login_user_fail_not_found(db_session, mock_UserLoginRequest):

    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.login(mock_UserLoginRequest)

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_USER_NOT_FOUND_USER


def test_login_user_fail_password_wrong(db_session, mock_user_on_db, mock_UserLoginRequest):

    login = UserLoginRequest(
        cpf=mock_user_on_db.cpf,
        password="654321"
    )

    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.login(login)

    assert e.value.status_code == 401
    assert e.value.detail == ERROR_USER_PASSWORD_WRONG