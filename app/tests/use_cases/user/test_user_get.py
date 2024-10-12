from fastapi import HTTPException
from pytest import raises


from controllers.user import UserUseCases
from database.models import UserModel
from schemas.user import UserResponse
def test_get_user_success(db_session, mock_UserRequest):

    uc = UserUseCases(db_session)

    db_session.add(UserModel(**mock_UserRequest.dict()))
    db_session.commit()

    user = uc.get(mock_UserRequest.cpf)

    assert isinstance(user, UserResponse)
    assert user.cpf == mock_UserRequest.cpf
    assert user.name == mock_UserRequest.name
    assert user.phone == mock_UserRequest.phone
    assert user.phone_optional == mock_UserRequest.phone_optional
    assert user.email == mock_UserRequest.email
    assert user.level == mock_UserRequest.level