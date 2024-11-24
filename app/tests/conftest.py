from pytest import fixture
from fastapi.testclient import TestClient


from constants.user import LEVEL
from database.connection import Session
from database.models import UserModel
from main import app
from schemas.address import AddressRequest
from schemas.user import (
    UserLoginRequest, 
    UserRequest, 
    UserUpdateRequest
)
from services.security.password import protect


@fixture
def api():
    return TestClient(app)

@fixture
def db_session():
    try:
        session = Session()

        session.query(UserModel).delete()

        session.commit()

        yield session

    finally:

        session.query(UserModel).delete()

        session.commit()

        session.close()


@fixture
def clean_data():
    
    session = Session()

    session.query(UserModel).delete()

    session.commit()

    session.close()


@fixture
def mock_address_data():
    data = {}
    data["state"] = "PI"
    data["city"] = "Teresina"
    data["neighborhood"] = "Centro"
    data["street"] = "Rua A"
    data["house_number"] = "123"
    data["complement"] = "Ultima Casa da Esquina"

    return data

@fixture
def mock_user_data(mock_address_data) -> dict:
    data = {}
    data["cpf"] = "123.456.789-00"
    data["name"] = "John Doe"
    data["birth_date"]="1990-01-01"
    data["gender"] = "M"
    data["phone"] = "90900000001"  # Número de telefone no formato correto
    data["phone_optional"] = "90900000000"  # Número de telefone no formato correto
    data["email"] = "test@example.com"
    data["password"] = "123456"
    data["level"] = 1
    data["address"] = AddressRequest(**mock_address_data)

    return data


@fixture
def mock_AddressRequest(mock_address_data) -> AddressRequest:
    return AddressRequest(**mock_address_data)

@fixture
def mock_UserRequest(mock_AddressRequest) -> UserRequest:
    return UserRequest(
        cpf="123.456.789-00",
        name="John Doe",
        birth_date="1990-01-01",
        gender="M",
        phone="(00) 90000-0000",
        email="john.doe@gmail.com",
        password="123456",
        level=LEVEL["parent"],
        address=AddressRequest(**mock_AddressRequest.dict())
    )

@fixture
def mock_user_on_db(db_session, mock_UserRequest) -> UserModel:
    
    request = UserRequest(**mock_UserRequest.dict())

    request.password = protect(request.password)

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
        password="654321",
        level=LEVEL["parent"],
        address=AddressRequest(
            state="PI",
            city="Picos",
            neighborhood="Junco",
            street="Rua A",
            house_number="123",
            complement="Ultima Casa"
        )
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