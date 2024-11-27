from pytest import fixture
from fastapi.testclient import TestClient


from constants.user import LEVEL
from database.connection import Session
from database.models import ClassModel, UserModel
from main import app
from schemas.address import Address
from schemas.base import (
    DaysOfWeek,
    EducationLevel,
    Shift
)
from schemas.classes import (
    ClassEventResponse,
    ClassRequest,
    Recurrences
)
from schemas.user import (
    UserDB,
    UserLoginRequest, 
    UserRequest, 
    UserUpdateRequest
)
from services.generator.ids import id_generate
from services.security.password import protect



@fixture
def api() -> TestClient:
    return TestClient(app)

@fixture
def db_session():
    try:
        session = Session()

        session.query(UserModel).delete()
        session.query(ClassModel).delete()

        session.commit()

        yield session

    finally:

        session.query(UserModel).delete()
        session.query(ClassModel).delete()

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
    data["address"] = Address(**mock_address_data)

    return data


@fixture
def mock_class_data():# -> dict:
    data = {}
    data["education_level"] = EducationLevel.ELEMENTARY.value
    data["name"] = "5° Ano"
    data["section"] = "A"
    data["shift"] = Shift.MORNING.value
    data["max_students"] = 20

    return data


@fixture
def mock_class_response_data(mock_class_data):# -> Any:# -> dict:
    data = mock_class_data.copy()
    data["id"] = "121"
    return data


@fixture
def mock_recurrences_data():
    data = {}
    data["day_of_week"] = DaysOfWeek.MONDAY.value
    data["start_time"] = "08:00"
    data["end_time"] = "09:00"

    return data


@fixture
def mock_class_event_request_data(mock_recurrences_data) -> dict:
    data = {}
    data["class_id"] = "1"
    data["disciplines_id"] = "2"
    data["teacher_id"] = "3"
    data["start_date"] = "2021-01-01"
    data["end_date"] = "2021-06-01"
    data["recurrences"] = [mock_recurrences_data]

    return data



@fixture
def mock_class_event_response_data(mock_class_event_request_data) -> dict:
    data = mock_class_event_request_data.copy()
    data["id"] = "12345"
    data["teacher_name"] = "John Doe"
    data["discipline_name"] = "Matemática"

    return data


@fixture
def mock_class_response_data(
    mock_class_data,
    mock_class_event_response_data
):
    data = mock_class_data.copy()

    data["class_info"] = "5° Ano - A"
    data["class_events"] = [mock_class_event_response_data.copy()]

    return data


@fixture
def mock_Address(mock_address_data) -> Address:
    return Address(**mock_address_data)


@fixture
def mock_UserRequest(mock_Address) -> UserRequest:
    return UserRequest(
        cpf="123.456.789-00",
        name="John Doe",
        birth_date="1990-01-01",
        gender="M",
        phone="(00) 90000-0000",
        email="john.doe@gmail.com",
        password="123456",
        level=LEVEL["parent"],
        address=Address(**mock_Address.dict())
    )

@fixture
def mock_user_on_db(db_session, mock_UserRequest) -> UserModel:
    
    request = UserRequest(**mock_UserRequest.dict())

    request.password = protect(request.password)

    to_db = UserDB(**request.dict(), **request.address.dict())

    user = UserModel(**to_db.dict())

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
        address=Address(
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


@fixture
def mock_ClassRequest(mock_class_data) -> ClassRequest:
    return ClassRequest(**mock_class_data)


@fixture
def mock_class_on_db(db_session, mock_ClassRequest) -> ClassModel:
    request = ClassRequest(**mock_ClassRequest.dict())

    to_db = ClassModel(
        id = id_generate(),
        **request.dict()
    )

    db_session.add(to_db)
    db_session.commit()

    return to_db


@fixture
def mock_ClassRequest_update() -> ClassRequest:
    
    return ClassRequest(
        education_level=EducationLevel.PRESCHOOL.value,
        name="1° Ano",
        section="A",
        shift=Shift.AFTERNOON.value,
        max_students=15
    )

@fixture
def mock_ClassEventResponse(mock_class_event_response_data) -> ClassEventResponse:
    return ClassEventResponse(**mock_class_event_response_data)


