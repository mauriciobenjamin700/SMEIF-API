from datetime import datetime
from fastapi.testclient import TestClient
from pytest import fixture


from database.connection import Session
from database.mapping.student import map_StudentRequest_to_ChildModel
from database.models import (
    ChildModel, 
    ChildParentsModel, 
    ClassEventModel, 
    ClassModel, 
    ClassStudentModel, 
    ClassTeacherModel, 
    DisciplinesModel, 
    NoteModel, 
    PresenceModel, 
    RecurrencesModel, 
    TeacherDisciplinesModel, 
    UserModel, 
    WarningModel
)
from main import app
from schemas.address import Address
from schemas.base import (
    DaysOfWeek,
    EducationLevel,
    Gender,
    Kinship,
    Shift,
    UserLevel
)
from schemas.classes import (
    ClassEventRequest,
    ClassEventResponse,
    ClassRequest,
    Recurrences
)
from schemas.child import(
    ChildRequest,
    StudentRequest
)
from schemas.disciplines import(
    DisciplineRequest,
    DisciplineResponse
)
from schemas.note import (
    NoteDB,
    NoteRequest,
    NoteUpdate
)
from schemas.teacher import (
    ClassTeacherRequest,
    TeacherDisciplinesRequest
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

        session.query(NoteModel).delete()
        session.query(WarningModel).delete()
        session.query(ClassStudentModel).delete()
        session.query(ChildParentsModel).delete()
        session.query(ChildModel).delete()
        session.query(PresenceModel).delete()
        session.query(ClassEventModel).delete()
        session.query(ClassTeacherModel).delete()
        session.query(TeacherDisciplinesModel).delete()
        session.query(UserModel).delete()
        session.query(ClassModel).delete()
        session.query(DisciplinesModel).delete()

        session.commit()

        yield session

    finally:

        session.query(NoteModel).delete()
        session.query(WarningModel).delete()
        session.query(ClassStudentModel).delete()
        session.query(ChildParentsModel).delete()
        session.query(ChildModel).delete()
        session.query(PresenceModel).delete()
        session.query(ClassEventModel).delete()
        session.query(ClassTeacherModel).delete()
        session.query(TeacherDisciplinesModel).delete()
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


@fixture
def mock_teacher_disciplines_request_data():
    data = {}
    data["user_cpf"] = "123.456.789-00"
    data["disciplines_id"] = ["1", "2", "3"]
    
    return data


@fixture
def mock_class_teacher_request_data():
    data = {}
    data["user_cpf"] = "123.456.789-00"
    data["classes_id"] = ["1", "2", "3"]

    return data



@fixture
def mock_StudentRequest_data(mock_address_data) -> dict:
    data = {}
    data["cpf"] = "123.456.789-00"
    data["name"] = "Student John Doe"
    data["birth_date"] = "2020-01-01"
    data["gender"] = Gender.MALE.value
    data["class_id"] = "1"
    data["address"] = mock_address_data.copy()
    data["kinship"] = Kinship.FATHER.value
    data["parent_cpf"] = "123.456.789-01"

    return data


@fixture
def mock_StudentResponse_data() -> dict:
    data = {
        "matriculation": "20240000001",
        "name": "Student John Doe",
        "class_info": "5° Ano A",
        "shift": Shift.MORNING.value
    }
    return data.copy()


@fixture
def mock_NoteRequest_data() -> dict:
    data = {}
    data["semester"] = 1
    data["aval_number"] = 1
    data["points"] = 7.5
    data["discipline_id"] = "12345"
    data["class_id"] = "12345"
    data["child_cpf"] = "123.456.789-00"

    return data.copy()


@fixture
def mock_NoteFilters_data() -> dict:
    data = {}
    data["semester"] = 1
    data["aval_number"] = 1
    data["discipline_id"] = "12345"
    data["class_id"] = "12345"
    data["child_cpf"] = "123.456.789-00"

    return data.copy()


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
    request.disciplines_id = [mock_discipline_on_db.id]

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


@fixture
def mock_ClassTeacherRequest(
    mock_teacher_on_db,
    mock_class_on_db
) -> ClassTeacherRequest:
    
    return ClassTeacherRequest(
        user_cpf=mock_teacher_on_db.cpf,
        classes_id=[mock_class_on_db.id]
)

@fixture
def mock_mock_TeacherDisciplinesRequest(
    mock_teacher_on_db,
    mock_discipline_on_db
) -> TeacherDisciplinesRequest:
    
    return TeacherDisciplinesRequest(
        user_cpf=mock_teacher_on_db.cpf,
        disciplines_id=[mock_discipline_on_db.id]
    )


@fixture
def mock_StudentRequest(
    mock_class_on_db,
    mock_parent_on_db
) -> dict:
    return StudentRequest(
        cpf="123.456.789-87",
        name="Pedro Vital Jr",
        birth_date="2010-01-01",
        gender="M",
        class_id=mock_class_on_db.id,
        address=Address(
            state="PI",
            city="Oeiras",
            neighborhood="Centro",
            street="Rua dos Cavalos",
            house_number="124"
        ),
        kinship=Kinship.FATHER.value,
        parent_cpf=mock_parent_on_db.cpf,

    )


@fixture
def mock_ChildRequest_update(
    mock_student_on_db,
    mock_StudentRequest
) -> ChildRequest:
    return ChildRequest(
        cpf=mock_student_on_db.cpf,
        name="Pedro Vital Junior",
        birth_date="2011-01-01",
        gender=Gender.MALE.value,
        address=mock_StudentRequest.address,
        dependencies="Precisa de ajuda para focar nos estudos, pois vive se distraindo."
    )


@fixture
def mock_NoteRequest(
    mock_discipline_on_db,
    mock_class_on_db,
    mock_student_on_db,
) -> NoteRequest:
    return NoteRequest(
        semester=1,
        aval_number=1,
        points=7.5,
        discipline_id=mock_discipline_on_db.id,
        class_id=mock_class_on_db.id,
        child_cpf=mock_student_on_db.cpf
    )


@fixture
def mock_NoteUpdate_points(
    mock_note_on_db
) -> NoteUpdate:
    return NoteUpdate(
        id=mock_note_on_db.id,
        points=9.3
    )


@fixture
def mock_NoteUpdate_aval_number(
    mock_note_on_db
):
    return NoteUpdate(
        id=mock_note_on_db.id,
        aval_number=2
    )

@fixture
def mock_NoteUpdate_points_and_aval_number(
    mock_note_on_db
):

    return NoteUpdate(
        id=mock_note_on_db.id,
        points=9.3,
        aval_number=2
    )


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
def mock_new_class_on_db(db_session):
    
    to_db = ClassModel(
        id = id_generate(),
        education_level=EducationLevel.ELEMENTARY.value,
        name="5° Ano",
        section="A",
        shift=Shift.MORNING.value,
        max_students=20
    )

    db_session.add(to_db)
    db_session.commit()

    return to_db


@fixture
def mock_list_class_on_db(db_session) -> list[ClassModel]:

    classes = [
        ClassModel(
            id=id_generate(),
            education_level=EducationLevel.ELEMENTARY.value,
            name="5° Ano",
            section="A",
            shift=Shift.MORNING.value,
            max_students=20
        ),
        ClassModel(
            id=id_generate(),
            education_level=EducationLevel.PRESCHOOL.value,
            name="1° Ano",
            section="A",
            shift=Shift.AFTERNOON.value,
            max_students=20
        ),
        ClassModel(
            id=id_generate(),
            education_level=EducationLevel.ELEMENTARY.value,
            name="7° Ano",
            section="A",
            shift=Shift.MORNING.value,
            max_students=20
        )
    ]

    db_session.add_all(classes)
    db_session.commit()

    return classes


@fixture
def mock_teacher_on_db(db_session) -> UserModel:

    user = UserModel(
        cpf="12345678966",
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


@fixture
def mock_teacher_discipline_on_db(
    db_session,
    mock_discipline_on_db, mock_teacher_on_db
) -> TeacherDisciplinesModel:

    teacher_discipline = TeacherDisciplinesModel(
        id=id_generate(),
        user_cpf=mock_teacher_on_db.cpf,
        discipline_id=mock_discipline_on_db.id
    )

    db_session.add(teacher_discipline)
    db_session.commit()

    return teacher_discipline


@fixture
def mock_class_teacher_on_db(
    db_session,
    mock_class_on_db,
    mock_teacher_on_db
) -> ClassTeacherModel:
    
    class_teacher = ClassTeacherModel(
        id=id_generate(),
        user_cpf=mock_teacher_on_db.cpf,
        class_id=mock_class_on_db.id
    )

    db_session.add(class_teacher)
    db_session.commit()

    return class_teacher


@fixture
def mock_parent_on_db(
    db_session
) -> UserModel:
    user = UserModel(
        cpf="12345678978",
        name="Pedro Vital",
        birth_date=datetime(1980, 1, 10),
        gender = Gender.MALE.value,
        phone="89912344321",
        email="pedrovital13@gmail.com",
        password=protect("123456"),
        level=UserLevel.PARENT.value,
        state="PI",
        city="Oeiras",
        neighborhood="Centro",
        street="Rua dos cavalos",
        house_number="124",
    )

    db_session.add(user)
    db_session.commit()

    return user


@fixture
def mock_new_parent_on_db(
    db_session
):
    
    parent = UserModel(
        cpf="123.321.123-32",
        name="José Maria",
        birth_date=datetime(1995, 9, 20),
        gender = Gender.MALE.value,
        phone="89912344322",
        email="josemaria@gmail.com",
        password=protect("123456"),
        level=UserLevel.PARENT.value,
        state="PI",
        city="Teresina",
        neighborhood="Barra Nova",
        street="Rua dos Bandeirantes",
        house_number="125"
    )
    
    db_session.add(parent)
    db_session.commit()
    
    return parent


@fixture
def mock_second_parent_on_db(
    db_session
):
    parent = UserModel(
        cpf="123.321.123-33",
        name="Maria R",
        birth_date=datetime(1995, 9, 20),
        gender = Gender.FEMALE.value,
        phone="89912344323",
        email="mariajose@gmail.com",
        password=protect("123456"),
        level=UserLevel.PARENT.value,
        state="PI",
        city="Teresina",
        neighborhood="Barra Nova",
        street="Rua dos Bandeirantes",
        house_number="126"
    )
    
    db_session.add(parent)
    db_session.commit()
    
    
    return parent


@fixture
def mock_student_on_db(
    db_session,
    mock_StudentRequest
) -> ChildModel:
    
    request = StudentRequest(**mock_StudentRequest.dict())
    
    model = map_StudentRequest_to_ChildModel(request)

    db_session.add(model)

    class_student = ClassStudentModel(
        id = id_generate(),
        class_id = request.class_id,
        child_cpf=request.cpf
    )

    db_session.add(class_student)

    child_parents = ChildParentsModel(
        id=id_generate(),
        kinship=request.kinship,
        child_cpf=request.cpf,
        parent_cpf=request.parent_cpf
    )

    db_session.add(child_parents)
    
    db_session.commit()

    return model


@fixture
def mock_student_on_db_with_max_parents(
    db_session,
    mock_student_on_db: ChildModel,
    mock_second_parent_on_db: UserModel
):
    student = mock_student_on_db
    parent = mock_second_parent_on_db

    child_parents = ChildParentsModel(
        id=id_generate(),
        kinship=Kinship.GRANDFATHER.value,
        child_cpf=student.cpf,
        parent_cpf=parent.cpf
    )

    db_session.add(child_parents)
    
    db_session.commit()

    return student


@fixture
def mock_note_on_db(
    db_session,
    mock_NoteRequest
) -> NoteModel:
    to_db = NoteDB(**mock_NoteRequest.dict())
    model = NoteModel(**to_db.dict())

    db_session.add(model)

    db_session.commit()

    return model


@fixture
def mock_note_on_db_list(
    db_session,
    mock_student_on_db: ChildModel,
    mock_discipline_on_db: DisciplinesModel,
    mock_class_on_db: ClassModel
):
    """
    4 notas do 1 semestre e uma do 2
    """
    student = mock_student_on_db
    discipline = mock_discipline_on_db
    class_ = mock_class_on_db

    notes = [
        NoteModel(
            id=id_generate(),
            semester=1,
            aval_number=1,
            points=7.8,
            discipline_id=discipline.id,
            class_id=class_.id,
            child_cpf=student.cpf
        )
        ,
        NoteModel(
            id=id_generate(),
            semester=1,
            aval_number=2,
            points=8.5,
            discipline_id=discipline.id,
            class_id=class_.id,
            child_cpf=student.cpf
        ),
        NoteModel(
            id=id_generate(),
            semester=1,
            aval_number=3,
            points=9,
            discipline_id=discipline.id,
            class_id=class_.id,
            child_cpf=student.cpf
        ),
        NoteModel(
            id=id_generate(),
            semester=1,
            aval_number=4,
            points=7,
            discipline_id=discipline.id,
            class_id=class_.id,
            child_cpf=student.cpf
        ),
        NoteModel(
            id=id_generate(),
            semester=2,
            aval_number=1,
            points=10,
            discipline_id=discipline.id,
            class_id=class_.id,
            child_cpf=student.cpf
        )
    ]


    db_session.add_all(notes)

    db_session.commit()

    return notes