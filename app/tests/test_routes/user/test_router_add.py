from constants.user import MESSAGE_USER_ADD_SUCCESS


def test_router_user_add_success(clean_data,api,mock_UserRequest):

    response = api.post("/user/add", json=mock_UserRequest.dict())

    assert response.status_code == 200
    data = response.json()

    assert data["detail"] == MESSAGE_USER_ADD_SUCCESS