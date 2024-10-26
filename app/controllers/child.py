from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.child import (
    MESSAGE_ADD_SUCESS, 
    MESSAGE_DELETE_SUCESS,
    ERROR_CPF_ALREADY_EXISTS,
    ERROR_NOT_FOUND_USER, 
    ERROR_NOT_FOUND_USERS, 
    ERROR_NOT_ID, 
    MESSAGE_UPDATE_FAIL, 
    MESSAGE_UPDATE_SUCESS
)
from controllers.base import Repository
from database.models import ChildModel, ChildParentsModel
from schemas.child import (
    ChildRequest,
    ChildResponse,
    ChildUpdateRequest
)
from utils.cryptography import (
    crypto
)
from utils.messages import (
    ServerError,
    SucessMessage,
    ErrorMessage
)


class ChildUseCases(Repository):
    """
    - Attributes:
        - db_session: Sessão de conexão com o banco de dados

    - Methods:
        - add
        - get
        - get_all
        - update
        - delete
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, request: ChildRequest) -> dict:
        """
        Adiciona um Aluno ao banco de dados

        - Args:
            - request: Objeto com os dados do aluno a ser adicionado.

        - Returns:
            - dict: {"detail": "Aluno cadastrado com sucesso"}

        - Raises:
            - HTTPException: 409 - CPF já cadastrado
            - HTTPException: 409 - Telefone já cadastrado
            - HTTPException: 409 - Email já cadastrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            self._check_existence(
                request.cpf, 
                request.matriculation
            )
            
            request.password = crypto(request.password)
            
            child = ChildModel(**request.dict())

            self.db_session.add(child)
            self.db_session.commit()

            return SucessMessage(MESSAGE_ADD_SUCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)

    def get(self, id: str)  -> ChildResponse:
        """
        Retorna os dados de um aluno específico

        - Args:
            - id: CPF do aluno a ser retornado
        
        - Returns:
            - ChildResponse: Objeto com os dados do aluno

        - Raises:
            - HTTPException: 400 - ID não informado
            - HTTPException: 404 - Aluno não encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            child = self._get(id)

            return self._map_ChildModel_to_ChildResponse(child)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)


    def get_all(self) -> list[ChildResponse]:
        """
        Retorna todos os alunos cadastrados

        - Args:
            - None

        - Returns:
            - list[ChildResponse]: Lista de objetos com os dados dos alunos

        - Raises:
            - HTTPException: 404 - Nenhum aluno encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            childs = self._get_all()

            return self._map_list_ChildModel_to_list_ChildResponse(childs)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)
        
    def get_all_by_parent(self) -> list[ChildResponse]:
        """
        Retorna todos os alunos cadastrados

        - Args:
            - None

        - Returns:
            - list[ChildResponse]: Lista de objetos com os dados dos alunos

        - Raises:
            - HTTPException: 404 - Nenhum aluno encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            childs = self._get_all_by_parent()

            return self._map_list_ChildModel_to_list_ChildResponse(childs)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)
        
    def update(self, id:str, request: ChildUpdateRequest) -> dict:
        """
        Atualiza os dados de um aluno

        - Args:
            - id: CPF do aluno a ser atualizado
            - request: Objeto com os dados a serem atualizados

        - Returns:
            - dict: {"detail": "Aluno atualizado com sucesso"}
            - dict: {"detail": "Nenhum dado foi atualizado"}

        - Raises:
            - HTTPException: 400 - ID não informado
            - HTTPException: 404 - Aluno não encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:
                
            child = self._get(id)

            updated = False

            for field, value in request.dict().items():

                if value:

                    if field == "password":

                        value = crypto(value)

                    value_in_field =  getattr(child, field)

                    if value != value_in_field:

                        setattr(child, field, value)
                        updated = True

            if updated:

                self.db_session.commit()
                self.db_session.refresh(child)

            return SucessMessage(MESSAGE_UPDATE_SUCESS) if updated else SucessMessage(MESSAGE_UPDATE_FAIL)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)

    def delete(self, id: str) -> dict:
        """
        Deleta um aluno

        - Args:
            - id: CPF do aluno a ser deletado

        - Returns:
            - dict: {"detail": "Aluno deletado com sucesso"}

        - Raises:
            - HTTPException: 400 - ID não informado
            - HTTPException: 404 - Aluno não encontrado
            - HTTPException: 500 - Erro no servidor
        """
        try:

            child = self._get(id)

            self.db_session.delete(child)
            self.db_session.commit()

            return SucessMessage(MESSAGE_DELETE_SUCESS)

        except HTTPException:
            raise

        except Exception as e:
            raise ServerError(e)
        
    def _check_existence(self, cpf: str | None) -> None:
            
            if cpf:
            
                child = self.db_session.query(ChildModel).filter_by(cpf=cpf).first()
        
                if child:
                    
                    raise ErrorMessage(409, ERROR_CPF_ALREADY_EXISTS)
            

    def _get(self, id: str) -> ChildModel:

        if not id:
            raise ErrorMessage(400, ERROR_NOT_ID)
        
        child = self.db_session.query(ChildModel).filter_by(cpf=id).first()

        if not child:
            raise ErrorMessage(404, ERROR_NOT_FOUND_USER)
        
        return child
    
    def _get_all(self) -> list[ChildModel]:

        childs = self.db_session.query(ChildModel).all()

        if not childs:
            raise ErrorMessage(404, ERROR_NOT_FOUND_USERS)
        
        return childs
    
    def _get_all_by_parent(self, parent: str) -> list[ChildModel]:
        childs = self.db_session.query(ChildModel).join(ChildParentsModel, ChildModel.cpf== ChildParentsModel.child_cpf).filter(ChildParentsModel.parent_cpf == parent)

        if not childs:
            raise ErrorMessage(404, ERROR_NOT_FOUND_USERS)
        
        return childs

    def _map_ChildModel_to_ChildResponse(self, child: ChildModel) -> ChildResponse:
        return ChildResponse(
            cpf=child.cpf,
            name=child.name,
            matriculation=child.matriculation
        )
    
    def _map_list_ChildModel_to_list_ChildResponse(self, childs: list[ChildModel]) -> list[ChildResponse]:
        return [self._map_ChildModel_to_ChildResponse(child) for child in childs]