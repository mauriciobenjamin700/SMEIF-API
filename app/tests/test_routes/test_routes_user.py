from constants.user import (
    MESSAGE_USER_ADD_SUCCESS,
    MESSAGE_USER_DELETE_SUCCESS,
    MESSAGE_USER_UPDATE_SUCCESS
)
from schemas.user import UserResponse
from services.security.tokens import decode_token


def test_router_user_add_success(clean_data,api,mock_UserRequest):

    response = api.post("/user/add", json=mock_UserRequest.dict())

    assert response.status_code == 200
    data = response.json()

    assert data["detail"] == MESSAGE_USER_ADD_SUCCESS


def test_router_user_delete(mock_user_on_db, api):
    
    response = api.delete(f"/user/delete?user_id={mock_user_on_db.cpf}")

    assert response.status_code == 200
    data = response.json()

    assert data["detail"] == MESSAGE_USER_DELETE_SUCCESS


from schemas.user import UserResponse

def test_router_user_get(mock_user_on_db, api):
    
    response = api.get(f"/user/get?user_id={mock_user_on_db.cpf}",)

    assert response.status_code == 200
    data = response.json()

    UserResponse(**data)




def test_router_user_list(mock_user_on_db, api):
    
    response = api.get("/user/list")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1

    UserResponse(**data[0])


def test_router_user_login_success(api,mock_user_on_db, mock_UserLoginRequest):

    response = api.post(f"/user/login?user_id={mock_user_on_db.cpf}", json=mock_UserLoginRequest.dict())

    assert response.status_code == 200
    data = response.json()

    token = decode_token(data["token"])

    UserResponse(**token)



def test_router_user_update(mock_user_on_db, mock_UserUpdateRequest_level,api):
    
    response = api.put(f"/user/update?user_id={mock_user_on_db.cpf}",json=mock_UserUpdateRequest_level.dict())

    assert response.status_code == 200
    data = response.json()

    assert data["detail"] == MESSAGE_USER_UPDATE_SUCCESS

    response = api.get(f"/user/get?user_id={mock_user_on_db.cpf}")

    assert response.status_code == 200

    data = response.json()

    UserResponse(**data)