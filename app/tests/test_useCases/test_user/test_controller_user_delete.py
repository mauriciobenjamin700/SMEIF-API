from fastapi import HTTPException
from pytest import raises


from constants.user import (
    ERROR_USER_NOT_FOUND_USER,
    ERROR_USER_REQUIRED_FIELD_CPF,
    MESSAGE_USER_DELETE_SUCCESS
)
from useCases.user import UserUseCases


def test_delete_user_success(db_session, mock_user_on_db):

    uc = UserUseCases(db_session)

    response = uc.delete(mock_user_on_db.cpf)

    assert response.detail == MESSAGE_USER_DELETE_SUCCESS


def test_delete_user_fail_no_id(db_session):

    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.delete(None)

    assert e.value.status_code == 400
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_CPF


def test_delete_user_fail_not_found(db_session):

    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.delete("None")

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_USER_NOT_FOUND_USER