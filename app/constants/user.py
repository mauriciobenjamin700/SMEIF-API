"""
- LEVEL
-
"""
LEVEL = {
    "parent": 1,
    "teacher": 2,
    "coordination": 3,
    "admin": 4
}
MESSAGE_ADD_SUCESS = "Usuário cadastrado com sucesso"
MESSAGE_UPDATE_SUCESS = "Usuário atualizado com sucesso"
MESSAGE_UPDATE_FAIL = "Nenhum dado foi atualizado"
MESSAGE_DELETE_SUCESS = "Usuário deletado com sucesso"

ERROR_NOT_ID = "ID não informado"
ERROR_NOT_FOUND_USER = "Usuário não encontrado"
ERROR_NOT_FOUND_USERS = "Nenhum usuário encontrado"
ERROR_PASSWORD_WRONG = "Senha inválida"
ERROR_CPF_ALREADY_EXISTS = "CPF já cadastrado"
ERROR_PHONE_ALREADY_EXISTS = "Telefone já cadastrado"
ERROR_EMAIL_ALREADY_EXISTS = "Email já cadastrado"

ERROR_PHONE_AND_OPTIONAL_PHONE_EQUALS = "Telefone e Telefone Opcional não podem ser iguais"

ERROR_USER_REQUIRED_FIELD_CPF = "CPF é obrigatório"
ERROR_USER_REQUIRED_FIELD_NAME = "Nome é obrigatório"
ERROR_USER_REQUIRED_FIELD_PHONE = "Telefone é obrigatório"