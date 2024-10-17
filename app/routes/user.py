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
    ADD_RESPONSES,
    DELETE_DESCRIPTION,
    DELETE_RESPONSE_DESCRIPTION,
    DELETE_RESPONSES,
    GET_DESCRIPTION,
    GET_RESPONSE_DESCRIPTION,
    GET_RESPONSES,
    LIST_DESCRIPTION,
    LIST_RESPONSE_DESCRIPTION,
    LIST_RESPONSES,
    LOGIN_DESCRIPTION,
    LOGIN_RESPONSE_DESCRIPTION,
    LOGIN_RESPONSES,
    UPDATE_DESCRIPTION,
    UPDATE_RESPONSE_DESCRIPTION,
    UPDATE_RESPONSES
)


router = APIRouter(prefix='/user', tags=['User'])

@router.post('/add', description=ADD_DESCRIPTION, response_description=ADD_RESPONSE_DESCRIPTION, responses=ADD_RESPONSES)
async def add_user(
    user: UserRequest,
    db_session: Session = Depends(db_session),
) -> dict:    

    uc = UserUseCases(db_session)

    response = uc.add(user)

    return response

@router.get("/get", description=GET_DESCRIPTION, response_description=GET_RESPONSE_DESCRIPTION, responses=GET_RESPONSES)
async def get_user(
    user_id: str,
    db_session: Session = Depends(db_session)
) -> UserResponse:

    uc = UserUseCases(db_session)

    response = uc.get(user_id)

    return response

@router.get("/list", description=LIST_DESCRIPTION, response_description=LIST_RESPONSE_DESCRIPTION, responses=LIST_RESPONSES)
async def list_users(
    db_session: Session = Depends(db_session)
) -> list[UserResponse]:

    uc = UserUseCases(db_session)

    response = uc.get_all()

    return response


@router.put("/update", description=UPDATE_DESCRIPTION, response_description=UPDATE_RESPONSE_DESCRIPTION, responses=UPDATE_RESPONSES)
async def update_user(
    user_id: str,
    update: UserUpdateRequest,
    db_session: Session = Depends(db_session)
) -> dict:

    uc = UserUseCases(db_session)

    response = uc.update(user_id, update)

    return response


@router.delete("/delete", description=DELETE_DESCRIPTION, response_description=DELETE_RESPONSE_DESCRIPTION, responses=DELETE_RESPONSES)
async def delete_user(
    user_id: str,
    db_session: Session = Depends(db_session)
) -> dict:
    
    uc = UserUseCases(db_session)

    response = uc.delete(user_id)

    return response


@router.post("/login", description=LOGIN_DESCRIPTION, response_description=LOGIN_RESPONSE_DESCRIPTION, responses=LOGIN_RESPONSES)
async def login(
    user: UserLoginRequest,
    db_session: Session = Depends(db_session)
) -> str:

    uc = UserUseCases(db_session)

    response = uc.login(user)

    return response