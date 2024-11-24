from datetime import datetime
from fastapi import HTTPException
from pytest import raises


from constants.base import (
    ERROR_INVALID_CPF, 
    ERROR_INVALID_EMAIL,
    ERROR_INVALID_FORMAT_BIRTH_DATE,
    ERROR_INVALID_FORMAT_GENDER, 
    ERROR_INVALID_PHONE, 
    ERROR_INVALID_PHONE_OPTIONAL
)
from constants.user import (
    ERROR_USER_INVALID_BIRTHDATE,
    ERROR_USER_INVALID_LEVEL,
    ERROR_USER_PHONE_AND_OPTIONAL_PHONE_EQUALS,
    ERROR_USER_REQUIRED_FIELD_BIRTH_DATE,
    ERROR_USER_REQUIRED_FIELD_CPF,
    ERROR_USER_REQUIRED_FIELD_EMAIL,
    ERROR_USER_REQUIRED_FIELD_GENDER,
    ERROR_USER_REQUIRED_FIELD_NAME,
    ERROR_USER_REQUIRED_FIELD_PASSWORD,
    ERROR_USER_REQUIRED_FIELD_PHONE
)
from schemas.user import (
    UserRequest,
    UserUpdateRequest,
    UserLoginRequest
)


def test_UserRequest_success(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    user = UserRequest(
        cpf=cpf,
        name=name,
        birth_date=birth_date,
        gender=gender,
        phone=phone,
        phone_optional=phone_optional,
        email=email,
        password=password,
        level=level,
        address=mock_AddressRequest
    )

    assert user.cpf == cpf.replace(".", "").replace("-", "")
    assert user.name == name
    assert user.birth_date == birth_date
    assert user.gender == gender
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password
    assert user.level == level
    assert user.address == mock_AddressRequest

def test_UserRequest_fail_cpf_none(mock_AddressRequest):
    cpf = None
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_CPF

def test_UserRequest_fail_cpf_spaces(mock_AddressRequest):
    cpf = "     "
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_CPF

def test_UserRequest_fail_cpf_validation(mock_AddressRequest):
    cpf = "123"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF


def test_UserRequest_fail_name_none(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = None
    birth_date="1990-01-01"
    gender = "M"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_NAME


def test_UserRequest_fail_name_spaces(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "    "
    birth_date="1990-01-01"
    gender = "M"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            birth_date=birth_date,
            gender = gender,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_NAME


def test_UserRequest_fail_birth_date_none(mock_user_data):

    data = mock_user_data
    data['birth_date'] = None

    with raises(HTTPException) as e:
        UserRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_BIRTH_DATE


def test_UserRequest_fail_birth_format(mock_user_data):

    data = mock_user_data
    data['birth_date'] = "10/11/2002"

    with raises(HTTPException) as e:
        UserRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_FORMAT_BIRTH_DATE


def test_UserRequest_fail_birth_date_young(mock_user_data):

    data = mock_user_data
    data['birth_date'] = datetime.now().strftime("%Y-%m-%d")
    print(data['birth_date'])

    with raises(HTTPException) as e:
        UserRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_INVALID_BIRTHDATE


def test_UserRequest_fail_gender_none(mock_user_data):
    
    data = mock_user_data
    data["gender"] = ""

    with raises(HTTPException) as e:
        UserRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_GENDER


def test_UserRequest_fail_gender_invalid(mock_user_data):
    
    data = mock_user_data
    data["gender"] = "LGBT"

    with raises(HTTPException) as e:
        UserRequest(**data)

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_FORMAT_GENDER


def test_UserRequest_fail_phone_none(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "john doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = None  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_PHONE


def test_UserRequest_fail_phone_spaces(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "     "   # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_PHONE

def test_UserRequest_fail_phone_validation(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "12312"   # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_PHONE


def test_UserRequest_success_with_no_optional_phone(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = ""  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    user = UserRequest(
        cpf=cpf,
        name=name,
        phone=phone,
        birth_date=birth_date,
        gender = gender,
        phone_optional=phone_optional,
        email=email,
        password=password,
        level=level,
        address=mock_AddressRequest
    )

    assert user.cpf == cpf.replace(".", "").replace("-", "")
    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password
    assert user.level == level
    assert user.address == mock_AddressRequest

def test_UserRequest_fail_option_phone_validation(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "89912345678"   # Número de telefone no formato correto
    phone_optional = "1234"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_PHONE_OPTIONAL


def test_UserRequest_fail_option_phone_equals_phone(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "89912345678"   # Número de telefone no formato correto
    phone_optional = "89912345678"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_PHONE_AND_OPTIONAL_PHONE_EQUALS



def test_UserRequest_fail_email_spaces(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = " "
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_EMAIL

def test_UserRequest_fail_email_validation(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "aaaa"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_EMAIL



def test_UserRequest_fail_password_spaces(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "example@gmail.com"
    password = "   "
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_PASSWORD


def test_UserRequest_fail_level_None(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "example@gmail.com"
    password = "12345"
    level = None

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_INVALID_LEVEL

def test_UserRequest_fail_level_invalid(mock_AddressRequest):
    cpf = "123.456.789-00"
    name = "John Doe"
    birth_date="1990-01-01"
    gender = "M"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "example@gmail.com"
    password = "12345"
    level = 10

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            birth_date=birth_date,
            gender = gender,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level,
            address=mock_AddressRequest
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_INVALID_LEVEL


def test_UserUpdateRequest_success(mock_AddressRequest):
    name = "John Doe"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "jhon.doe@gmail.com"
    password = "123456"
    level=2

    user = UserUpdateRequest(
        name=name,
        phone=phone,
        phone_optional=phone_optional,
        email=email,
        password=password,
        level=level,
        address=mock_AddressRequest
    )

    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password

def test_UserUpdateRequest_success_no_name():
    name = ""
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "jhon.doe@gmail.com"
    password = "123456"

    user = UserUpdateRequest(
        name=name,
        phone=phone,
        phone_optional=phone_optional,
        email=email,
        password=password
    )

    assert user.name == ''
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password

def test_UserUpdateRequest_success_no_phone():
    name = "John Doe"
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "jhon.doe@gmail.com"
    password = "123456"

    user = UserUpdateRequest(
        name=name,
        phone_optional=phone_optional,
        email=email,
        password=password
    )

    assert user.name == name
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password

def test_UserUpdateRequest_success_no_optional_phone():
    name = "John Doe"
    phone = "90900000001"  # Número de telefone no formato correto
    email = "jhon.doe@gmail.com"
    password = "123456"

    user = UserUpdateRequest(
        name=name,
        phone=phone,
        email=email,
        password=password
    )

    assert user.name == name
    assert user.phone == phone
    assert user.email == email
    assert user.password == password

def test_UserUpdateRequest_success_no_email():
    name = "John Doe"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    password = "123456"

    user = UserUpdateRequest(
        name=name,
        phone=phone,
        phone_optional=phone_optional,
        password=password
    )

    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.password == password

def test_UserUpdateRequest_success_no_password():
    name = "John Doe"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "jhon.doe@gmail.com"

    user = UserUpdateRequest(
        name=name,
        phone=phone,
        phone_optional=phone_optional,
        email=email
    )

    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email



def test_UserLoginRequest_success():
    cpf = "123.456.789-00"
    password = "123456"

    user = UserLoginRequest(
        cpf=cpf,
        password=password
    )

    assert user.cpf == cpf.replace(".", "").replace("-", "")
    assert user.password == password

def test_UserLoginRequest_fail_no_cpf():
    cpf = ""
    password = "123456"

    with raises(HTTPException) as e:
        UserLoginRequest(
            cpf=cpf,
            password=password
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_CPF

def test_UserLoginRequest_fail_invalid_cpf():
    cpf = "123"
    password = "123456"

    with raises(HTTPException) as e:
        UserLoginRequest(
            cpf=cpf,
            password=password
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_INVALID_CPF


def test_UserLoginRequest_fail_no_password():
    cpf = "123.456.789-00"
    password = ""

    with raises(HTTPException) as e:
        UserLoginRequest(
            cpf=cpf,
            password=password
        )

    assert e.value.status_code == 422
    assert e.value.detail == ERROR_USER_REQUIRED_FIELD_PASSWORD