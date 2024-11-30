from datetime import datetime
from pytest import fixture
from fastapi.testclient import TestClient


from database.connection import Session
from database.models import ClassEventModel, ClassModel, ClassTeacherModel, DisciplinesModel, RecurrencesModel, UserModel
from main import app
from schemas.address import Address
from schemas.base import (
    DaysOfWeek,
    EducationLevel,
    Gender,
    Shift,
    UserLevel
)
from schemas.classes import (
    ClassEventRequest,
    ClassEventResponse,
    ClassRequest,
    Recurrences
)
from schemas.disciplines import(
    DisciplineRequest,
    DisciplineResponse
)
from schemas.user import (
    UserDB,
    UserLoginRequest, 
    UserRequest, 
    UserUpdateRequest
)
from services.generator.ids import id_generate
from services.security.password import protect
from utils.format import unformat_date



@fixture
def api() -> TestClient:
    return TestClient(app)

@fixture
def db_session():
    try:
        session = Session()

        session.query(ClassEventModel).delete()
        session.query(ClassTeacherModel).delete()
        session.query(UserModel).delete()
        session.query(ClassModel).delete()
        session.query(DisciplinesModel).delete()

        session.commit()

        yield session

    finally:

        session.query(ClassEventModel).delete()
        session.query(ClassTeacherModel).delete()
        session.query(UserModel).delete()
        session.query(ClassModel).delete()
        session.query(DisciplinesModel).delete()

        session.commit()

        session.close()


@fixture
def clean_data():
    
    session = Session()

    session.query(UserModel).delete()

    session.commit()

    session.close()

############################ DATA ############################
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
    data["disciplines_id"] = ["2", "3"]
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
def mock_discipline_request_data():
    data = {}
    data["name"] = "Matemática"

    return data


@fixture
def mock_discipline_response_data(mock_discipline_request_data) -> dict:
    data = mock_discipline_request_data.copy()
    data["id"] = "12345"

    return data




############################ SCHEMAS ############################


@fixture
def mock_UserUpdateRequest() -> UserUpdateRequest:

    update = UserUpdateRequest(
        name="Teacher Jane Doe",
        phone_optional="(00) 91111-1111",
        phone="(00) 90000-0066",
        email="jane.doe@gmail.com",
        password="654321",
        level=UserLevel.TEACHER.value,
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
        level=UserLevel.TEACHER.value
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
        level=UserLevel.PARENT.value,
        address=Address(**mock_Address.dict())
    )


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
def mock_DisciplineRequest(mock_discipline_request_data) -> DisciplineRequest:

    return DisciplineRequest(**mock_discipline_request_data)


@fixture
def mock_DisciplineResponse(mock_discipline_response_data) -> DisciplineResponse:

    return DisciplineResponse(**mock_discipline_response_data)


@fixture
def mock_ClassEventRequest(
    mock_class_event_request_data,
    mock_class_on_db,
    mock_ClassTeacher_on_db,
    mock_discipline_on_db,
) -> ClassEventRequest:
    request =  ClassEventRequest(**mock_class_event_request_data)

    request.class_id = mock_class_on_db.id
    request.teacher_id = mock_ClassTeacher_on_db.id
    request.disciplines_id = mock_discipline_on_db.id

    return request


@fixture
def mock_ClassEventUpdate(
    mock_class_event_request_data,
    mock_class_on_db,
    mock_ClassTeacher_on_db,
    mock_discipline_on_db,
) -> ClassEventRequest:
    
    request =  ClassEventRequest(**mock_class_event_request_data)

    request.class_id = mock_class_on_db.id
    request.teacher_id = mock_ClassTeacher_on_db.id
    request.disciplines_id = mock_discipline_on_db.id

    request.start_date = "2026-01-01"
    request.end_date = "2026-06-01"
    

    return request

@fixture
def mock_ClassEventResponse(mock_class_event_response_data) -> ClassEventResponse:
    return ClassEventResponse(**mock_class_event_response_data)

@fixture
def mock_Recurrences_list() -> list[Recurrences]:
    
    recurrences = [
        Recurrences(
            day_of_week=DaysOfWeek.WEDNESDAY.value,
            start_time="14:00",
            end_time="15:00"
        ),
        Recurrences(
            day_of_week=DaysOfWeek.FRIDAY.value,
            start_time="15:20",
            end_time="16:20"
        )
    ]

    return recurrences

############################ MODELS ############################

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
def mock_teacher_on_db(db_session) -> UserModel:

    user = UserModel(
        cpf="123.456.789-66",
        name="Teacher Doe",
        birth_date=datetime(1990, 1, 1),
        gender = Gender.MALE.value,
        phone="89912344320",
        email="teacher@professor.com",
        password=protect("123456"),
        level=UserLevel.TEACHER.value,
        state="PI",
        city="Picos",
        neighborhood="Junco",
        street="Rua A",
        house_number="123",
        complement="Ultima Casa"
    )

    db_session.add(user)

    db_session.commit()

    return user


@fixture
def mock_ClassTeacher_on_db(
    db_session,
    mock_teacher_on_db,
    mock_class_on_db
) -> ClassTeacherModel:
    
    to_db = ClassTeacherModel(
        id=id_generate(), 
        user_cpf=mock_teacher_on_db.cpf,
        class_id=mock_class_on_db.id
    )

    db_session.add(to_db)
    db_session.commit()

    return to_db


@fixture
def mock_discipline_on_db(db_session, mock_DisciplineRequest) -> DisciplinesModel:

    request = DisciplineRequest(**mock_DisciplineRequest.dict())

    to_db = DisciplinesModel(
        id = id_generate(),
        **request.dict()
    )

    db_session.add(to_db)
    db_session.commit()

    return to_db


@fixture
def mock_class_event_on_db(
    db_session,
    mock_class_on_db,
    mock_ClassTeacher_on_db,
    mock_discipline_on_db,
    mock_class_event_request_data
) -> ClassEventModel:

    request = ClassEventRequest(**mock_class_event_request_data)

    to_db = ClassEventModel(
        id = id_generate(),
        class_id=mock_class_on_db.id,
        teacher_id=mock_ClassTeacher_on_db.id,
        discipline_id=mock_discipline_on_db.id,
        start_date= unformat_date(request.start_date, portuguese=False),
        end_date=unformat_date(request.end_date, portuguese=False)
    )

    recurrence = RecurrencesModel(
        id=id_generate(),
        class_event_id=to_db.id,
        day_of_week=request.recurrences[0].day_of_week,
        start_time=request.recurrences[0].start_time,
        end_time=request.recurrences[0].end_time
    )

    db_session.add(to_db)

    db_session.add(recurrence)

    db_session.commit()

    return to_db


@fixture
def mock_recurrence_on_db(
    db_session,
    mock_class_event_on_db
) -> RecurrencesModel:

    recurrence = RecurrencesModel(
        id=id_generate(),
        class_event_id=mock_class_event_on_db.id,
        day_of_week=DaysOfWeek.WEDNESDAY.value,
        start_time="13:00",
        end_time="14:00"
    )

    db_session.add(recurrence)

    db_session.commit()

    return recurrence