from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.user import (
    MESSAGE_USER_ADD_SUCCESS, 
    MESSAGE_USER_DELETE_SUCCESS,
    ERROR_USER_CPF_ALREADY_EXISTS,
    ERROR_USER_EMAIL_ALREADY_EXISTS,
    ERROR_USER_NOT_FOUND_USER, 
    ERROR_USER_NOT_FOUND_USERS, 
    ERROR_USER_NOT_ID, 
    ERROR_USER_PASSWORD_WRONG,
    ERROR_USER_PHONE_ALREADY_EXISTS, 
    MESSAGE_UPDATE_FAIL, 
    MESSAGE_UPDATE_SUCCESS
)
from controllers.base import Repository
from database.models import UserModel
from schemas.base import BaseMessage
from schemas.user import (
    UserLoginRequest,
    UserRequest,
    UserResponse,
    UserUpdateRequest
)
from app.utils.security.cryptography import (
    crypto,
    verify
)
from app.utils.messages.messages import (
    ServerError,
    SucessMessage,
    ErrorMessage
)
from app.services.security.tokens import encode_token


class UserUseCases(Repository):
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

            self._check_existence(
                request.cpf, 
                request.phone, 
                request.email
            )
            
            request.password = crypto(request.password)
            
            user = UserModel(**request.dict())

            self.db_session.add(user)
            self.db_session.commit()

            return SucessMessage(MESSAGE_USER_ADD_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)

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

            user = self._get(id)

            return self._map_UserModel_to_UserResponse(user)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)


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

            users = self._get_all()

            return self._map_list_UserModel_to_list_UserResponse(users)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)
        
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
            - HTTPException: 400 - ID não informado
            - HTTPException: 404 - Usuário não encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:
                
            user = self._get(id)

            updated = False

            for field, value in request.dict().items():

                if value:

                    if field == "password":

                        value = crypto(value)

                    value_in_field =  getattr(user, field)

                    if value != value_in_field:

                        setattr(user, field, value)
                        updated = True

            if updated:

                self.db_session.commit()
                self.db_session.refresh(user)

            return SucessMessage(MESSAGE_UPDATE_SUCCESS) if updated else SucessMessage(MESSAGE_UPDATE_FAIL)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)

    def delete(self, id: str) -> BaseMessage:
        """
        Deleta um usuário

        - Args:
            - id: CPF do usuário a ser deletado

        - Returns:
            - dict: {"detail": "Usuário deletado com sucesso"}

        - Raises:
            - HTTPException: 400 - ID não informado
            - HTTPException: 404 - Usuário não encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            user = self._get(id)

            self.db_session.delete(user)
            self.db_session.commit()

            return SucessMessage(MESSAGE_USER_DELETE_SUCCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)
        
    def login(self, acess: UserLoginRequest) -> str:
        """
        Realiza o login de um usuário

        - Args:
            - acess: Objeto com os dados de login

        - Returns:
            - str: Token de autenticação

        - Raises:
            - HTTPException: 404 - Usuário não encontrado
            - HTTPException: 401 - Senha inválida
            - HTTPException: 500 - Erro no servidor
        """
        try:

            user = self.db_session.query(UserModel).filter_by(cpf=acess.cpf).first()

            if not user:
                raise ErrorMessage(404, ERROR_USER_NOT_FOUND_USER)

            if not verify(acess.password, user.password):
                raise ErrorMessage(401, ERROR_USER_PASSWORD_WRONG)
            
            data = self._map_UserModel_to_UserResponse(user)
            
            token = encode_token(data.dict())
            
            return token

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)
        
    def _check_existence(self, cpf: str | None, phone: str | None, email: str | None) -> None:
            
            if cpf:
            
                user = self.db_session.query(UserModel).filter_by(cpf=cpf).first()
        
                if user:
                    
                    raise ErrorMessage(409, ERROR_USER_CPF_ALREADY_EXISTS)
                
            if phone:
            
                user = self.db_session.query(UserModel).filter_by(phone=phone).first()

                if user:
                    
                    raise ErrorMessage(409, ERROR_USER_PHONE_ALREADY_EXISTS)
                
            if email:

                user = self.db_session.query(UserModel).filter_by(email=email).first()
                
                if user:
                    
                    raise ErrorMessage(409, ERROR_USER_EMAIL_ALREADY_EXISTS)

            

    def _get(self, id: str) -> UserModel:

        if not id:
            raise ErrorMessage(400, ERROR_USER_NOT_ID)
        
        user = self.db_session.query(UserModel).filter_by(cpf=id).first()

        if not user:
            raise ErrorMessage(404, ERROR_USER_NOT_FOUND_USER)
        
        return user
    
    def _get_all(self) -> list[UserModel]:

        users = self.db_session.query(UserModel).all()

        if not users:
            raise ErrorMessage(404, ERROR_USER_NOT_FOUND_USERS)
        
        return users
    
    def _map_UserModel_to_UserResponse(self, user: UserModel) -> UserResponse:
        return UserResponse(
            cpf=user.cpf,
            name=user.name,
            phone=user.phone,
            phone_optional=user.phone_optional,
            email=user.email,
            level=user.level
        )
    
    def _map_list_UserModel_to_list_UserResponse(self, users: list[UserModel]) -> list[UserResponse]:
        return [self._map_UserModel_to_UserResponse(user) for user in users]