from fastapi import HTTPException
from sqlalchemy.orm import Session


from controllers.base import Repository
from database.models import UserModel
from schemas.user import (
    UserLoginRequest,
    UserRequest,
    UserResponse,
    UserUpdateRequest
)
from utils.cryptography import (
    crypto,
    verify
)
from services.tokens import encode_token


class UserUseCases(Repository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, request: UserRequest) -> dict:
        """
        Adiciona um Usuário ao banco de dados

        - Args:
            - request: Objeto com os dados do usuário a ser adicionado.

        - Returns:
            - dict: {"detail": "Usuário cadastrado com sucesso"}

        - Raises:
            - HTTPException: 400 - ID não informado
            - HTTPException: 404 - Usuário não encontrado
            - HTTPException: 409 - Usuário já cadastrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            user = self._get(request.cpf)

            if user:
                raise HTTPException(status_code=409, detail="Usuário já cadastrado")
            
            request.password = crypto(request.password)
            
            user = UserModel(**request.dict())

            self.db_session.add(user)
            self.db_session.commit()

            return {"detail": "Usuário cadastrado com sucesso"}

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")

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
            raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")


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
            raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")
        
    def update(self, id:str, request: UserUpdateRequest) -> dict:
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
    
                    setattr(user, field, value)
                    updated = True

            if updated:

                self.db_session.commit()
                self.db_session.refresh(user)

            return {"detail": "Usuário atualizado com sucesso"} if updated else {"detail": "Nenhum dado foi atualizado"}

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")

    def delete(self, id: str) -> None:
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

            return {"detail": "Usuário deletado com sucesso"}

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")
        
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

            user = self.db_session.query(UserModel).filter_by(login=acess.login).first()

            if not user:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")

            if not verify(acess.password, user.password):
                raise HTTPException(status_code=401, detail="Senha inválida")
            

            data = self._map_UserModel_to_UserResponse(user)
            
            token = encode_token(data.dict())
            
            return token

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")

    def _get(self, id: str) -> UserModel:

        if not id:
            raise HTTPException(status_code=400, detail="ID não informado")
        
        user = self.db_session.query(UserModel).filter_by(cpf=id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return user
    
    def _get_all(self) -> list[UserModel]:

        users = self.db_session.query(UserModel).all()

        if not users:
            raise HTTPException(status_code=404, detail="Nenhum usuário encontrado")
        
        return users
    
    def _map_UserModel_to_UserResponse(self, user: UserModel) -> UserResponse:
        return UserResponse(
            cpf=user.cpf,
            name=user.name,
            phone=user.phone,
            phone_optional=user.phone_optional,
            email=user.email
        )
    
    def _map_list_UserModel_to_list_UserResponse(self, users: list[UserModel]) -> list[UserResponse]:
        return [self._map_UserModel_to_UserResponse(user) for user in users]