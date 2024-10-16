from fastapi import (
    APIRouter, 
    Depends
)
from sqlalchemy.orm import Session


from controllers.user import UserUseCases
from schemas.user import(
    UserRequest,
    UserResponse,
    UserUpdateRequest,
    UserLoginRequest
)
from services.session import db_session
from routes.docs.user import (
    ADD_DESCRIPTION,
    ADD_RESPONSE_DESCRIPTION,
    ADD_RESPONSES
)


router = APIRouter(prefix='/client', tags=['Client'])

@router.post('/add', description=ADD_DESCRIPTION, response_description=ADD_RESPONSE_DESCRIPTION, responses=ADD_RESPONSES)
async def add_clients(
    user: UserRequest,
    db_session: Session = Depends(db_session),
) -> dict:    

    uc = UserUseCases(db_session)

    response = uc.add(user)

    return response