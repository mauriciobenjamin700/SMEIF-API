from fastapi import HTTPException
from pytest import raises


from database.models import UserModel
from constants.user import (
    ERROR_NOT_FOUND_USERS, 
    UPDATE_MESSAGE_SUCESS
)
from controllers.user import UserUseCases
from schemas.user import UserResponse
from utils.cryptography import verify

def test_update_user_sucess(db_session, mock_user_on_db,mock_UserUpdateRequest):
    
    uc = UserUseCases(db_session)

    response = uc.update(mock_user_on_db.cpf, mock_UserUpdateRequest)

    assert response["detail"]  == UPDATE_MESSAGE_SUCESS["detail"]

    user = db_session.query(UserModel).filter_by(cpf=mock_user_on_db.cpf).first()

    assert user.name == mock_UserUpdateRequest.name
    assert user.phone == mock_UserUpdateRequest.phone
    assert user.phone_optional == mock_UserUpdateRequest.phone_optional
    assert user.email == mock_UserUpdateRequest.email
    assert verify(mock_UserUpdateRequest.password, user.password)

def test_update_user_level(db_session, mock_user_on_db, mock_UserUpdateRequest_level):
    
    uc = UserUseCases(db_session)

    response = uc.update(mock_user_on_db.cpf, mock_UserUpdateRequest_level)

    assert response["detail"]  == UPDATE_MESSAGE_SUCESS["detail"]

    user = db_session.query(UserModel).filter_by(cpf=mock_user_on_db.cpf).first()


    assert user.level == mock_UserUpdateRequest_level.level
