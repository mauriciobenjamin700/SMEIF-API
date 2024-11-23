from fastapi import HTTPException
from pytest import raises


from database.models import UserModel
from constants.user import (
    ERROR_USER_NOT_FOUND_USER,
    ERROR_USER_NOT_ID,
    MESSAGE_UPDATE_SUCCESS, 
    MESSAGE_UPDATE_FAIL
)
from controllers.user import UserUseCases
from schemas.user import (
    UserResponse,
    UserUpdateRequest
)
from app.utils.security.cryptography import verify


def test_update_user_sucess(db_session, mock_user_on_db,mock_UserUpdateRequest):
    
    uc = UserUseCases(db_session)

    response = uc.update(mock_user_on_db.cpf, mock_UserUpdateRequest)

    assert response.detail == MESSAGE_UPDATE_SUCCESS

    user = db_session.query(UserModel).filter_by(cpf=mock_user_on_db.cpf).first()

    assert user.name == mock_UserUpdateRequest.name
    assert user.phone == mock_UserUpdateRequest.phone
    assert user.phone_optional == mock_UserUpdateRequest.phone_optional
    assert user.email == mock_UserUpdateRequest.email
    assert verify(mock_UserUpdateRequest.password, user.password)

def test_update_user_level(db_session, mock_user_on_db, mock_UserUpdateRequest_level):
    
    uc = UserUseCases(db_session)

    response = uc.update(mock_user_on_db.cpf, mock_UserUpdateRequest_level)

    assert response.detail  == MESSAGE_UPDATE_SUCCESS

    user = db_session.query(UserModel).filter_by(cpf=mock_user_on_db.cpf).first()


    assert user.level == mock_UserUpdateRequest_level.level

def test_update_user_not_updated(db_session, mock_user_on_db):

    uc = UserUseCases(db_session)

    update = UserUpdateRequest(
        name=mock_user_on_db.name,
        phone=mock_user_on_db.phone,
        phone_optional=mock_user_on_db.phone_optional,
        email=mock_user_on_db.email,
    )

    response = uc.update(mock_user_on_db.cpf, update)

    assert response.detail  == MESSAGE_UPDATE_FAIL


def test_update_user_no_id(db_session, mock_user_on_db, mock_UserUpdateRequest):

    uc = UserUseCases(db_session)

    with raises(HTTPException) as e:
        uc.update(None, mock_UserUpdateRequest)

    assert e.value.status_code == 400
    assert e.value.detail == ERROR_USER_NOT_ID

def test_update_user_not_found(db_session, mock_user_on_db, mock_UserUpdateRequest):
    
        uc = UserUseCases(db_session)
    
        with raises(HTTPException) as e:
            uc.update("12345678901", mock_UserUpdateRequest)
    
        assert e.value.status_code == 404
        assert e.value.detail == ERROR_USER_NOT_FOUND_USER