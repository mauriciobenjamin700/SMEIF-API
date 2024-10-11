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
