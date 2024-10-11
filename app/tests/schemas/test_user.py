from fastapi import HTTPException
from pytest import raises



from schemas.user import UserRequest


def test_UserRequest_sucess():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    login = "john.doe"
    password = "123456"
    level = 1

    user = UserRequest(
        cpf=cpf,
        name=name,
        phone=phone,
        phone_optional=phone_optional,
        email=email,
        login=login,
        password=password,
        level=level
    )

    assert user.cpf == cpf.replace(".", "").replace("-", "")
    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.login == login
    assert user.password == password
    assert user.level == level

def test_UserRequest_fail_cpf_none():
    cpf = None
    name = "John Doe"
    phone = "90900000001"  # Número de telefone no formato correto
    phone_optional = "90900000000"  # Número de telefone no formato correto
    email = "test@example.com"
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    user = UserRequest(
        cpf=cpf,
        name=name,
        phone=phone,
        phone_optional=phone_optional,
        email=email,
        login=login,
        password=password,
        level=level
    )

    assert user.cpf == cpf.replace(".", "").replace("-", "")
    assert user.name == name
    assert user.phone == phone
    assert user.phone_optional == phone_optional
    assert user.email == email
    assert user.login == login
    assert user.password == password
    assert user.level == level


def test_UserRequest_fail_option_phone_validation():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   # Número de telefone no formato correto
    phone_optional = "1234"  # Número de telefone no formato correto
    email = "test@example.com"
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Email inválido"


def test_UserRequest_fail_login_spaces():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "example@gmail.com"
    login = "    "
    password = "123456"
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Campo Login vazio"


def test_UserRequest_fail_password_spaces():
    cpf = "123.456.789-00"
    name = "John Doe"
    phone = "89912345678"   
    phone_optional = "89912345679"  
    email = "example@gmail.com"
    login = "john.doe"
    password = "   "
    level = 1

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "12345"
    level = None

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
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
    login = "john.doe"
    password = "12345"
    level = 10

    with raises(HTTPException) as e:
        UserRequest(
            cpf=cpf,
            name=name,
            phone=phone,
            phone_optional=phone_optional,
            email=email,
            login=login,
            password=password,
            level=level
        )

    assert e.value.status_code == 400
    assert e.value.detail == "Nível de Acesso inválido"