from pytest import fixture


from constants.user import LEVEL
from database.connection import Session
from database.models import UserModel
from schemas.user import UserLoginRequest, UserRequest, UserUpdateRequest
from utils.cryptography import crypto

@fixture
def db_session():
    try:
        session = Session()

        session.query(UserModel).delete()

        yield session

    finally:

        session.query(UserModel).delete()

        session.close()


@fixture
def mock_UserRequest() -> UserRequest:
    return UserRequest(
        cpf="123.456.789-00",
        name="John Doe",
        phone="(00) 90000-0000",
        email="john.doe@gmail.com",
        password="123456",
        level=LEVEL["parent"]
    )

@fixture
def mock_user_on_db(db_session, mock_UserRequest) -> UserModel:
    
    request = UserRequest(**mock_UserRequest.dict())

    request.password = crypto(request.password)

    user = UserModel(**request.dict())

    db_session.add(user)
    db_session.commit()

    return user


@fixture
def mock_UserUpdateRequest() -> UserUpdateRequest:

    update = UserUpdateRequest(
        name="Jane Doe",
        phone_optional="(00) 91111-1111",
        phone="(00) 90000-0066",
        email="jane.doe@gmail.com",
        password="654321"
    )

    return update

@fixture
def mock_UserUpdateRequest_level() -> UserUpdateRequest:

    update = UserUpdateRequest(
        level=LEVEL["teacher"]
    )

    return update


@fixture
def mock_UserLoginRequest(mock_UserRequest) -> UserLoginRequest:

    login = UserLoginRequest(
        cpf=mock_UserRequest.cpf,
        password=mock_UserRequest.password
    )

    return login