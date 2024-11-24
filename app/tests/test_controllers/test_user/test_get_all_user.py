from fastapi import HTTPException
from pytest import raises


from constants.user import ERROR_USER_NOT_FOUND_USERS
from controllers.user import UserController
from schemas.user import UserResponse


def test_get_all_user_success(db_session, mock_user_on_db):

    uc = UserController(db_session)

    users = uc.get_all()

    assert isinstance(users, list)

    user = users[0]
    
    assert isinstance(user, UserResponse)
    assert user.cpf == mock_user_on_db.cpf
    assert user.name == mock_user_on_db.name
    assert user.phone == mock_user_on_db.phone
    assert user.phone_optional == mock_user_on_db.phone_optional
    assert user.email == mock_user_on_db.email
    assert user.level == mock_user_on_db.level


def test_get_all_user_fail_not_found(db_session):
    uc = UserController(db_session)

    with raises(HTTPException) as e:
        uc.get_all()

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_USER_NOT_FOUND_USERS