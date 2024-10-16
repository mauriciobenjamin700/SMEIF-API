"""
- LEVEL
- ADD_MESSAGE
- UPDATE_MESSAGE_SUCESS
- UPDATE_MESSAGE_FAIL
- DELETE_MESSAGE
- ERROR_NOT_ID
- ERROR_NOT_FOUND_USER
- ERROR_NOT_FOUND_USERS
- ERROR_PASSWORD_WRONG
- ERROR_CPF_ALREADY_EXISTS
- ERROR_PHONE_ALREADY_EXISTS
- ERROR_EMAIL_ALREADY_EXISTS
"""
LEVEL = {
    "parent": 1,
    "teacher": 2,
    "coordination": 3,
    "admin": 4
}

ADD_MESSAGE = {"detail": "Usuário cadastrado com sucesso"}
UPDATE_MESSAGE_SUCESS = {"detail": "Usuário atualizado com sucesso"}
UPDATE_MESSAGE_FAIL = {"detail": "Nenhum dado foi atualizado"}
DELETE_MESSAGE = {"detail": "Usuário deletado com sucesso"}

ERROR_NOT_ID = "ID não informado"
ERROR_NOT_FOUND_USER = "Usuário não encontrado"
ERROR_NOT_FOUND_USERS = "Nenhum usuário encontrado"
ERROR_PASSWORD_WRONG = "Senha inválida"
ERROR_CPF_ALREADY_EXISTS = "CPF já cadastrado"
ERROR_PHONE_ALREADY_EXISTS = "Telefone já cadastrado"
ERROR_EMAIL_ALREADY_EXISTS = "Email já cadastrado"
