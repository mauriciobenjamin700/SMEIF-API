from constants.user import MESSAGE_USER_DELETE_SUCCESS
from schemas.user import UserResponse

def test_router_user_delete(mock_user_on_db, api):
    
    response = api.delete(f"/user/delete?user_id={mock_user_on_db.cpf}")

    assert response.status_code == 200
    data = response.json()

    assert data["detail"] == MESSAGE_USER_DELETE_SUCCESS
