from fastapi import HTTPException
from pytest import raises


from constants.base import ERROR_INVALID_CPF, ERROR_INVALID_FORMAT_BIRTH_DATE, ERROR_INVALID_FORMAT_GENDER, ERROR_INVALID_FORMAT_SHIFT
from constants.child import(
    ERROR_CHILD_INVALID_FIELD_BIRTH_DATE,
    ERROR_CHILD_INVALID_FIELD_KINSHIP,
    ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE,
    ERROR_CHILD_REQUIRED_FIELD_CLASS_ID,
    ERROR_CHILD_REQUIRED_FIELD_CPF,
    ERROR_CHILD_REQUIRED_FIELD_GENDER,
    ERROR_CHILD_REQUIRED_FIELD_KINSHIP,
    ERROR_CHILD_REQUIRED_FIELD_NAME,
    ERROR_CHILD_REQUIRED_FIELD_PARENT_CPF
)
from schemas.address import Address
from schemas.child import(
    ChildRequest,
    StudentRequest,
    StudentResponse
)
from utils.format import(
    unformat_cpf
)


def test_schema_StudentRequest_success(
    mock_StudentRequest_data
):
    request = StudentRequest(**mock_StudentRequest_data)

    assert request.cpf == unformat_cpf(mock_StudentRequest_data["cpf"])
    assert request.name == mock_StudentRequest_data["name"]
    assert request.birth_date == mock_StudentRequest_data["birth_date"]
    assert request.gender == mock_StudentRequest_data["gender"]
    assert request.class_id == mock_StudentRequest_data["class_id"]
    assert request.address != mock_StudentRequest_data["address"]
    assert request.address == Address(**mock_StudentRequest_data["address"])
    assert request.kinship == mock_StudentRequest_data["kinship"]
    assert request.parent_cpf == unformat_cpf(mock_StudentRequest_data["parent_cpf"])
    assert request.complement == None


def test_schema_StudentRequest_no_cpf(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["cpf"] = "  "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_CPF


def test_schema_StudentRequest_fail_invalid_cpf(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["cpf"] = "123.456.789-0"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF


def test_schema_StudentRequest_no_name(mock_StudentRequest_data):
    mock_StudentRequest_data["name"] = " "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_NAME


def test_schema_StudentRequest_no_birth_date(mock_StudentRequest_data):
    mock_StudentRequest_data["birth_date"] = " "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE


def test_schema_StudentRequest_invalid_format_birth_date(mock_StudentRequest_data):
    mock_StudentRequest_data["birth_date"] = "01/01/2021"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_FORMAT_BIRTH_DATE


def test_schema_StudentRequest_invalid_birth_date_is_adult(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["birth_date"] = "2000-01-01"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_INVALID_FIELD_BIRTH_DATE


def test_schema_StudentRequest_no_gender(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["gender"] = " "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_GENDER


def test_schema_StudentRequest_invalid_gender(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["gender"] = "Transformer"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_FORMAT_GENDER


def test_schema_StudentRequest_no_class_id(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["class_id"] = " "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_CLASS_ID


def test_schema_StudentRequest_no_class_id(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["kinship"] = " "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_KINSHIP


def test_schema_StudentRequest_no_class_id(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["kinship"] = "sla"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_INVALID_FIELD_KINSHIP


def test_schema_StudentRequest_no_parent_cpf(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["parent_cpf"] = "  "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_PARENT_CPF


def test_schema_StudentRequest_fail_invalid_parent_cpf(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["parent_cpf"] = "123.456.789-0"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF


def test_schema_StudentResponse_success(
    mock_StudentResponse_data
):

    data = mock_StudentResponse_data.copy()

    response = StudentResponse(**data)


    assert response.matriculation == data["matriculation"]
    assert response.name == data["name"]
    assert response.class_info == data["class_info"]
    assert response.shift == data["shift"]


def test_schema_student_invalid_shift(mock_StudentResponse_data):
    mock_StudentResponse_data["shift"] = "Noite"

    with raises(HTTPException) as e:
        StudentResponse(**mock_StudentResponse_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_FORMAT_SHIFT


def test_schema_ChildRequest_success(
    mock_StudentRequest_data
):
    request = ChildRequest(**mock_StudentRequest_data)

    assert request.cpf == unformat_cpf(mock_StudentRequest_data["cpf"])
    assert request.name == mock_StudentRequest_data["name"]
    assert request.birth_date == mock_StudentRequest_data["birth_date"]
    assert request.gender == mock_StudentRequest_data["gender"]
    assert request.address != mock_StudentRequest_data["address"]
    assert request.address == Address(**mock_StudentRequest_data["address"])
    assert request.dependencies == None


def test_schema_ChildRequest_no_cpf(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["cpf"] = "  "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_CPF


def test_schema_ChildRequest_fail_invalid_cpf(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["cpf"] = "123.456.789-0"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF


def test_schema_ChildRequest_no_name(mock_StudentRequest_data):
    mock_StudentRequest_data["name"] = " "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_NAME


def test_schema_ChildRequest_no_birth_date(mock_StudentRequest_data):
    mock_StudentRequest_data["birth_date"] = " "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE


def test_schema_ChildRequest_invalid_format_birth_date(mock_StudentRequest_data):
    mock_StudentRequest_data["birth_date"] = "01/01/2021"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_FORMAT_BIRTH_DATE


def test_schema_ChildRequest_invalid_birth_date_is_adult(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["birth_date"] = "2000-01-01"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_INVALID_FIELD_BIRTH_DATE


def test_schema_ChildRequest_no_gender(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["gender"] = " "

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_CHILD_REQUIRED_FIELD_GENDER


def test_schema_ChildRequest_invalid_gender(
    mock_StudentRequest_data
):
    mock_StudentRequest_data["gender"] = "Transformer"

    with raises(HTTPException) as e:
        StudentRequest(**mock_StudentRequest_data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_FORMAT_GENDER