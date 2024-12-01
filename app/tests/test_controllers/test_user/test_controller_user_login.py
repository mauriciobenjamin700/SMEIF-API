from fastapi import HTTPException
from pytest import raises


from constants.user import (
    ERROR_USER_NOT_FOUND_USER,
    ERROR_USER_PASSWORD_WRONG
)
from controllers.user import UserController
from schemas.user import AccessToken, UserLoginRequest, UserResponse
from services.security.tokens import decode_token
from utils.format import (
    format_cpf,
    format_date,
    format_phone
)


def test_login_user_success(db_session, mock_user_on_db, mock_UserLoginRequest):

    uc = UserController(db_session)

    response = uc.login(mock_UserLoginRequest)

    assert isinstance(response, AccessToken)

    data = decode_token(response.token)

    user = UserResponse(**data)

    assert user.cpf == format_cpf(mock_user_on_db.cpf)
    assert user.name == mock_user_on_db.name
    assert user.birth_date == format_date(mock_user_on_db.birth_date)
    assert user.phone == format_phone(mock_user_on_db.phone)
    assert user.email == mock_user_on_db.email
    assert user.level == mock_user_on_db.level
    assert user.state == mock_user_on_db.state
    assert user.city == mock_user_on_db.city
    assert user.neighborhood == mock_user_on_db.neighborhood
    assert user.street == mock_user_on_db.street
    assert user.house_number == mock_user_on_db.house_number


def test_login_user_fail_not_found(db_session, mock_UserLoginRequest):

    uc = UserController(db_session)

    with raises(HTTPException) as e:
        uc.login(mock_UserLoginRequest)

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_USER_NOT_FOUND_USER


def test_login_user_fail_password_wrong(db_session, mock_user_on_db, mock_UserLoginRequest):

    login = UserLoginRequest(
        cpf=mock_user_on_db.cpf,
        password="654321"
    )

    uc = UserController(db_session)

    with raises(HTTPException) as e:
        uc.login(login)

    assert e.value.status_code == 401
    assert e.value.detail == ERROR_USER_PASSWORD_WRONG