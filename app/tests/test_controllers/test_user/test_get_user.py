from fastapi import HTTPException
from pytest import raises


from constants.user import (
    ERROR_NOT_FOUND_USER, 
    ERROR_NOT_ID
)
from controllers.user import UserUseCases
from schemas.user import UserResponse


def test_get_user_success(db_session, mock_user_on_db):

    uc = UserUseCases(db_session)

    user = uc.get(mock_user_on_db.cpf)

    assert isinstance(user, UserResponse)
    assert user.cpf == mock_user_on_db.cpf
    assert user.name == mock_user_on_db.name
    assert user.phone == mock_user_on_db.phone
    assert user.phone_optional == mock_user_on_db.phone_optional
    assert user.email == mock_user_on_db.email
    assert user.level == mock_user_on_db.level


def test_get_user_fail_no_id(db_session):
    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.get(None)

    assert e.value.status_code == 400
    assert e.value.detail == ERROR_NOT_ID


def test_get_user_fail_not_found(db_session):
    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.get("999.999.999-99")

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_NOT_FOUND_USER