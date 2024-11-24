from fastapi import HTTPException
from pytest import raises


from constants.user import (
    ERROR_USER_NOT_ID,
    ERROR_USER_NOT_FOUND_USER,
    MESSAGE_USER_DELETE_SUCCESS
)
from controllers.user import UserController


def test_delete_user_success(db_session, mock_user_on_db):

    uc = UserController(db_session)

    response = uc.delete(mock_user_on_db.cpf)

    assert response.detail == MESSAGE_USER_DELETE_SUCCESS


def test_delete_user_fail_no_id(db_session):

    uc = UserController(db_session)

    with raises(HTTPException) as e:
        uc.delete(None)

    assert e.value.status_code == 400
    assert e.value.detail == ERROR_USER_NOT_ID


def test_delete_user_fail_not_found(db_session):

    uc = UserController(db_session)

    with raises(HTTPException) as e:
        uc.delete("None")

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_USER_NOT_FOUND_USER