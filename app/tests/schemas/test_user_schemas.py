from fastapi import HTTPException
from pytest import raises


from schemas.user import (
    UserRequest,
    UserUpdateRequest,
    UserLoginRequest
)


def test_UserRequest_sucess():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    user = UserRequest(
        cpf=cpf,
        name=name,
        phone=phone,
        phone_optional=phone_optional,
        email=email,
        password=password,
        level=level
    )

    assert user.cpf == cpf.replace(".", "").replace("-", "")
    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password
    assert user.level == level

def test_UserRequest_fail_cpf_none():
    cpf = None
    name = "John Doe"
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
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo CPF vazio"

def test_UserRequest_fail_cpf_spaces():
    cpf = "     "
    name = "John Doe"
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
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo CPF vazio"

def test_UserRequest_fail_cpf_validation():
    cpf = "123"
    name = "John Doe"
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
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "CPF inválido"


def test_UserRequest_fail_name_none():
    cpf = "123.456.789-00"
    name = None
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
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo Nome vazio"


def test_UserRequest_fail_name_spaces():
    cpf = "123.456.789-00"
    name = "    "
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
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo Nome vazio"


def test_UserRequest_fail_phone_none():
    cpf = "123.456.789-00"
    name = "jhon doe"
    phone = None  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo Telefone vazio"


def test_UserRequest_fail_phone_spaces():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "     "   # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo Telefone vazio"

def test_UserRequest_fail_phone_validation():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "12312"   # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Número de telefone inválido. Deve conter 11 dígitos no formato correto (XX9XXXXXXXX)"


def test_UserRequest_sucess_with_no_optional_phone():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = ""  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    user = UserRequest(
        cpf=cpf,
        name=name,
        phone=phone,
        phone_optional=phone_optional,
        email=email,
        password=password,
        level=level
    )

    assert user.cpf == cpf.replace(".", "").replace("-", "")
    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password
    assert user.level == level


def test_UserRequest_fail_option_phone_validation():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   # Número de telefone no formato correto
    phone_optional = "1234"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Número de telefone inválido. Deve conter 11 dígitos no formato correto (XX9XXXXXXXX)"


def test_UserRequest_fail_option_phone_equals_phone():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   # Número de telefone no formato correto
    phone_optional = "89912345678"  # Número de telefone no formato correto
    email = "test@example.com"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Telefone e Telefone Opcional não podem ser iguais"



def test_UserRequest_fail_email_spaces():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = " "
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo E-mail vazio"

def test_UserRequest_fail_email_validation():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "aaaa"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Email inválido"



def test_UserRequest_fail_password_spaces():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "example@gmail.com"
    password = "   "
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo Senha vazio"


def test_UserRequest_fail_level_None():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "example@gmail.com"
    password = "12345"
    level = None

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Nível de Acesso inválido"

def test_UserRequest_fail_level_invalid():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "example@gmail.com"
    password = "12345"
    level = 10

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Nível de Acesso inválido"


def test_UserUpdateRequest_sucess():
    name = "John Doe"
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

    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password

def test_UserUpdateRequest_sucess_no_name():
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

    assert user.name == None
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.password == password

def test_UserUpdateRequest_sucess_no_phone():
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

def test_UserUpdateRequest_sucess_no_optional_phone():
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

def test_UserUpdateRequest_sucess_no_email():
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

def test_UserUpdateRequest_sucess_no_password():
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



def test_UserLoginRequest_sucess():
    cpf = "123.456.789-00"
    password = "123456"

    user = UserLoginRequest(
        cpf=cpf,
        password=password
    )

    assert user.cpf == cpf.replace(".", "").replace("-", "")
    assert user.password == password

# TODO: Testar todos os casos de login

def test_UserLoginRequest_fail_no_cpf():
    cpf = ""
    password = "123456"

    with raises(HTTPException) as e:
        UserLoginRequest(
            cpf=cpf,
            password=password
        )

    assert e.value.status_code == 400
    assert e.value.detail == "CPF não informado"

def test_UserLoginRequest_fail_invalid_cpf():
    cpf = "123"
    password = "123456"

    with raises(HTTPException) as e:
        UserLoginRequest(
            cpf=cpf,
            password=password
        )

    assert e.value.status_code == 400
    assert e.value.detail == "CPF inválido"


def test_UserLoginRequest_fail_no_password():
    cpf = "123.456.789-00"
    password = ""

    with raises(HTTPException) as e:
        UserLoginRequest(
            cpf=cpf,
            password=password
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Senha não informada"