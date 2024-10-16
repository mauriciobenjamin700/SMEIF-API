from fastapi import HTTPException
from pytest import raises


from constants.user import ADD_MESSAGE
from controllers.user import UserUseCases
from database.models import UserModel
from schemas.user import UserRequest
from utils.cryptography import verify

def test_add_user_success(db_session, mock_UserRequest):
    uc = UserUseCases(db_session)

    user = UserRequest(**mock_UserRequest.dict())

    response = uc.add(user)

    assert response["detail"] == ADD_MESSAGE["detail"]

    user_in_db = db_session.query(UserModel).filter(UserModel.cpf == user.cpf).first()

    assert user_in_db.cpf == user.cpf
    assert user_in_db.name == user.name
    assert user_in_db.phone == user.phone
    assert user_in_db.phone_optional == user.phone_optional
    assert user_in_db.email == user.email
    assert verify(mock_UserRequest.password, user_in_db.password)
    assert user_in_db.level == user.level


def test_add_user