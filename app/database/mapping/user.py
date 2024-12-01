from database.models import UserModel
from schemas.user import UserResponse
from utils.format import (
    format_date, 
    format_phone
)


def map_UserModel_to_UserResponse(user: UserModel) -> UserResponse:
    """
    Converte um usuário do banco de dados para um objeto UserResponse
    """
    return UserResponse(
        cpf=user.cpf,
        name=user.name,
        birth_date=user.birth_date,
        gender=user.gender,
        phone=user.phone,
        phone_optional= user.phone_optional,
        email=user.email,
        level=user.level,
        state=user.state,
        city=user.city,
        neighborhood=user.neighborhood,
        street=user.street,
        house_number=user.house_number,
        complement=user.complement
    )