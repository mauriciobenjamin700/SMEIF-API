from fastapi import (
    APIRouter, 
    Depends
)
from sqlalchemy.orm import Session


from useCases.user import UserUseCases
from schemas.user import(
    AccessToken,
    UserRequest,
    UserResponse,
    UserUpdateRequest,
    UserLoginRequest
)
from schemas.base import BaseMessage
from services.session import db_session
from routes.docs.user import (
    ADD_DESCRIPTION,
    ADD_RESPONSES,
    DELETE_DESCRIPTION,
    DELETE_RESPONSES,
    GET_DESCRIPTION,
    GET_RESPONSES,
    LIST_DESCRIPTION,
    LIST_RESPONSES,
    LOGIN_DESCRIPTION,
    LOGIN_RESPONSES,
    UPDATE_DESCRIPTION,
    UPDATE_RESPONSES
)


router = APIRouter(prefix='/user', tags=['User'])

@router.post('/add', description=ADD_DESCRIPTION, responses=ADD_RESPONSES)
async def add_user(
    user: UserRequest,
    db_session: Session = Depends(db_session),
) -> BaseMessage:    

    uc = UserUseCases(db_session)

    response = uc.add(user)

    return response

@router.get("/get", description=GET_DESCRIPTION, responses=GET_RESPONSES)
async def get_user(
    user_id: str,
    db_session: Session = Depends(db_session)
) -> UserResponse:

    uc = UserUseCases(db_session)

    response = uc.get(user_id)

    return response

@router.get("/list", description=LIST_DESCRIPTION, responses=LIST_RESPONSES)
async def list_users(
    db_session: Session = Depends(db_session)
) -> list[UserResponse]:

    uc = UserUseCases(db_session)

    response = uc.get_all()

    return response


@router.put("/update", description=UPDATE_DESCRIPTION, responses=UPDATE_RESPONSES)
async def update_user(
    user_id: str,
    update: UserUpdateRequest,
    db_session: Session = Depends(db_session)
) -> BaseMessage:

    uc = UserUseCases(db_session)

    response = uc.update(user_id, update)

    return response


@router.delete("/delete", description=DELETE_DESCRIPTION, responses=DELETE_RESPONSES)
async def delete_user(
    user_id: str,
    db_session: Session = Depends(db_session)
) -> BaseMessage:
    
    uc = UserUseCases(db_session)

    response = uc.delete(user_id)

    return response


@router.post("/login", description=LOGIN_DESCRIPTION, responses=LOGIN_RESPONSES)
async def login(
    user: UserLoginRequest,
    db_session: Session = Depends(db_session)
) -> AccessToken:

    uc = UserUseCases(db_session)

    response = uc.login(user)

    return response