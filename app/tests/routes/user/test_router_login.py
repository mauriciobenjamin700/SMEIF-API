from constants.user import MESSAGE_ADD_SUCESS
from services.tokens import decode_token
from schemas.user import UserResponse


def test_router_user_login_sucess(api,mock_user_on_db, mock_UserLoginRequest):

    response = api.post(f"/user/login?user_id={mock_user_on_db.cpf}", json=mock_UserLoginRequest.dict())

    assert response.status_code == 200
    data = response.json()

    token = decode_token(data)

    user = UserResponse(**token)

    assert user.cpf == mock_user_on_db.cpf
    assert user.name == mock_user_on_db.name
    assert user.phone == mock_user_on_db.phone
    assert user.phone_optional == mock_user_on_db.phone_optional
    assert user.email == mock_user_on_db.email
    assert user.level == mock_user_on_db.level

