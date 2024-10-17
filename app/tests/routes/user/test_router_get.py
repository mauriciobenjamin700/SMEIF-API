from schemas.user import UserResponse

def test_router_user_get(mock_user_on_db, api):
    
    response = api.get(f"/user/get?user_id={mock_user_on_db.cpf}",)

    assert response.status_code == 200
    data = response.json()

    user = UserResponse(**data)


    assert user.cpf == mock_user_on_db.cpf
    assert user.name == mock_user_on_db.name
    assert user.phone == mock_user_on_db.phone
    assert user.phone_optional == mock_user_on_db.phone_optional
    assert user.email == mock_user_on_db.email
    assert user.level == mock_user_on_db.level