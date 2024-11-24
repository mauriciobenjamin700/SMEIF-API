from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.user import (
    MESSAGE_USER_ADD_SUCCESS, 
    MESSAGE_USER_DELETE_SUCCESS,
    ERROR_USER_PASSWORD_WRONG,
    MESSAGE_USER_UPDATE_FAIL, 
    MESSAGE_USER_UPDATE_SUCCESS
)
from database.models import UserModel
from database.queries.existence import check_user_existence
from database.queries.get import get_user_by_cpf
from database.queries.get_all import get_all_users
from schemas.base import BaseMessage
from schemas.user import (
    AccessToken,
    UserDB,
    UserLoginRequest,
    UserRequest,
    UserResponse,
    UserUpdateRequest
)
from services.security.password import (
    protect,
    verify
)
from services.security.tokens import encode_token
from utils.format import format_date, format_phone
from utils.messages.success import Success
from utils.messages.error import (
    Server,
    Unauthorized
)


class UserController():
    """
    - Attributes:
        - db_session: Sessão de conexão com o banco de dados

    - Methods:
        - add
        - get
        - get_all
        - update
        - delete
        - login
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, request: UserRequest) -> BaseMessage:
        """
        Adiciona um Usuário ao banco de dados

        - Args:
            - request: Objeto com os dados do usuário a ser adicionado.

        - Returns:
            - dict: {"detail": "Usuário cadastrado com sucesso"}

        - Raises:
            - HTTPException: 409 - CPF já cadastrado
            - HTTPException: 409 - Telefone já cadastrado
            - HTTPException: 409 - Email já cadastrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            check_user_existence(self.db_session, request.cpf, request.phone, request.email)
            
            request.password = protect(request.password)

            to_db = UserDB(**request.dict(), **request.address.dict())
            
            user = UserModel(**to_db.dict())

            self.db_session.add(user)
            self.db_session.commit()

            return Success(MESSAGE_USER_ADD_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    def get(self, id: str)  -> UserResponse:
        """
        Retorna os dados de um usuário específico

        - Args:
            - id: CPF do usuário a ser retornado
        
        - Returns:
            - UserResponse: Objeto com os dados do usuário

        - Raises:
            - HTTPException: 400 - ID não informado
            - HTTPException: 404 - Usuário não encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            user = get_user_by_cpf(self.db_session,id)
            return self._map_UserModel_to_UserResponse(user)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)


    def get_all(self) -> list[UserResponse]:
        """
        Retorna todos os usuários cadastrados

        - Args:
            - None

        - Returns:
            - list[UserResponse]: Lista de objetos com os dados dos usuários

        - Raises:
            - HTTPException: 404 - Nenhum usuário encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            users = get_all_users(self.db_session)

            return self._map_list_UserModel_to_list_UserResponse(users)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        
    def update(self, id:str, request: UserUpdateRequest) -> BaseMessage:
        """
        Atualiza os dados de um usuário

        - Args:
            - id: CPF do usuário a ser atualizado
            - request: Objeto com os dados a serem atualizados

        - Returns:
            - dict: {"detail": "Usuário atualizado com sucesso"}
            - dict: {"detail": "Nenhum dado foi atualizado"}

        - Raises:
            - HTTPException: 400 - CPF é obrigatório
            - HTTPException: 404 - Usuário não encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:
                
            user = get_user_by_cpf(self.db_session, id)

            updated = False

            for field, value in request.dict().items():

                if value:

                    if field == "password":

                        value = protect(value)

                    elif field == "address": # Endereço é um objeto, por isso temos que iterar sobre ele e seus atributos
                            
                        for address_field, address_value in value.items(): # Quando o campo endereço é fragmentado, ele vira um dict

                            if address_value:

                                value_in_field =  getattr(user, address_field)

                                if address_value != value_in_field:

                                    setattr(user, address_field, address_value)
                                    updated = True

                        continue # Depois de atualizar o endereço, o campo address não tem mais valor e será ignorado
    

                    value_in_field =  getattr(user, field)

                    if value != value_in_field:

                        setattr(user, field, value)
                        updated = True

            if updated:

                self.db_session.commit()
                self.db_session.refresh(user)

            return Success(MESSAGE_USER_UPDATE_SUCCESS) if updated else Success(MESSAGE_USER_UPDATE_FAIL)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    def delete(self, id: str) -> BaseMessage:
        """
        Deleta um usuário

        - Args:
            - id: CPF do usuário a ser deletado

        - Returns:
            - dict: {"detail": "Usuário deletado com sucesso"}

        - Raises:
            - HTTPException: 400 - CPF é obrigatório
            - HTTPException: 404 - Usuário não encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            user = get_user_by_cpf(self.db_session, id)

            self.db_session.delete(user)
            self.db_session.commit()

            return Success(MESSAGE_USER_DELETE_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)
        
    def login(self, access: UserLoginRequest) -> AccessToken:
        """
        Realiza o login de um usuário

        - Args:
            - access: Objeto com os dados de login

        - Returns:
            - str: Token de autenticação

        - Raises:
            - HTTPException: 404 - Usuário não encontrado
            - HTTPException: 401 - Senha inválida
            - HTTPException: 500 - Erro no servidor
        """
        try:

            user = get_user_by_cpf(self.db_session, access.cpf)

            if not verify(access.password, user.password):

                raise Unauthorized(ERROR_USER_PASSWORD_WRONG)
            
            data = self._map_UserModel_to_UserResponse(user)
            
            token = encode_token(data.dict())
            
            return AccessToken(token=token)

        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)

    
    def _map_UserModel_to_UserResponse(self, user: UserModel) -> UserResponse:
        return UserResponse(
            cpf=user.cpf,
            name=user.name,
            birth_date=format_date(user.birth_date),
            gender=user.gender,
            phone=format_phone(user.phone),
            phone_optional= format_phone(user.phone_optional) if user.phone_optional else "",
            email=user.email,
            level=user.level,
            state=user.state,
            city=user.city,
            neighborhood=user.neighborhood,
            street=user.street,
            house_number=user.house_number,
            complement=user.complement if user.complement else ""
        )
    
    def _map_list_UserModel_to_list_UserResponse(self, users: list[UserModel]) -> list[UserResponse]:
        return [self._map_UserModel_to_UserResponse(user) for user in users]