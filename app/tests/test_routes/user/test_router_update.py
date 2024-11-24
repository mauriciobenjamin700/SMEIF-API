from constants.user import MESSAGE_USER_UPDATE_SUCCESS
from schemas.user import UserResponse


def test_router_user_update(mock_user_on_db, mock_UserUpdateRequest_level,api):
    
    response = api.put(f"/user/update?user_id={mock_user_on_db.cpf}",json=mock_UserUpdateRequest_level.dict())

    assert response.status_code == 200
    data = response.json()

    assert data["detail"] == MESSAGE_USER_UPDATE_SUCCESS

    response = api.get(f"/user/get?user_id={mock_user_on_db.cpf}")

    assert response.status_code == 200

    data = response.json()

    user = UserResponse(**data)


    assert user.cpf == mock_user_on_db.cpf
    assert user.name == mock_user_on_db.name
    assert user.phone == mock_user_on_db.phone
    assert user.phone_optional == mock_user_on_db.phone_optional
    assert user.email == mock_user_on_db.email
    assert user.level == mock_UserUpdateRequest_level.level