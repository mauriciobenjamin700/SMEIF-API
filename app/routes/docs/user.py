from constants.user import MESSAGE_ADD_SUCESS
from utils.messages import ErrorMessage, SucessMessage, generate_error_responses_from_exceptions


ADD_DESCRIPTION = """
Add a new client in the database
             
- Example:
             
        {
            "cpf": "123.456.789-00",
            "name": "John Doe",
            "phone": "(00) 90000-0000",
            "phone_optional": "(00) 9000-0001",
            "email": " jhon.doe@example.com",
            "password": 123,
            "level": 1
        }
             
"""
ADD_RESPONSE_DESCRIPTION = f"""


            "detail": "{MESSAGE_ADD_SUCESS}"
        

"""

ADD_RESPONSES = generate_error_responses_from_exceptions(
    [
        ErrorMessage(409, "CPF já cadastrado"),
        ErrorMessage(409, "Telefone já cadastrado"),
        ErrorMessage(409, "Email já cadastrado"),
        ErrorMessage(500, "Erro no servidor"),
        ErrorMessage(400, "Jhon derrubou o servidor")
    ]
)

# ADD_RESPONSES = {
#     409: {
#         "description": "Conflito de dados",
#         "content": {
#             "application/json": {
#                 "examples": {
#                     "cpf_conflict": {
#                         "summary": "CPF já cadastrado",
#                         "value": {"detail": "CPF já cadastrado"}
#                     },
#                     "phone_conflict": {
#                         "summary": "Telefone já cadastrado",
#                         "value": {"detail": "Telefone já cadastrado"}
#                     },
#                     "email_conflict": {
#                         "summary": "Email já cadastrado",
#                         "value": {"detail": "Email já cadastrado"}
#                     }
#                 }
#             }
#         }
#     },
#     500: {
#         "description": "Erro no servidor",
#         "content": {
#             "application/json": {
#                 "example": {"detail": "Erro interno do servidor"}
#             }
#         }
#     }
# }