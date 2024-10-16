from fastapi import HTTPException
from pytest import raises


from controllers.user import UserUseCases
from database.models import UserModel
from schemas.user import UserResponse
def test_get_user_success(db_session, mock_user_on_db, mock_UserRequest):

    uc = UserUseCases(db_session)

    users = uc.get_all()

    assert isinstance(users, list)

    user = users[0]
    
    assert isinstance(user, UserResponse)
    assert user.cpf == mock_UserRequest.cpf
    assert user.name == mock_UserRequest.name
    assert user.phone == mock_UserRequest.phone
    assert user.phone_optional == mock_UserRequest.phone_optional
    assert user.email == mock_UserRequest.email
    assert user.level == mock_UserRequest.level