from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.disciplines import (
    ERROR_DISCIPLINES_ADD_CONFLICT,
    MESSAGE_DISCIPLINE_ADD_SUCCESS,
    MESSAGE_DISCIPLINE_DELETE_SUCCESS
)
from database.models import DisciplinesModel
from database.queries.existence import discipline_exists
from database.queries.get import get_discipline_by_name
from database.queries.get_all import get_all_disciplines
from schemas.base import BaseMessage
from schemas.disciplines import(
    DisciplineRequest,
    DisciplineResponse
)
from services.generator.ids import id_generate
from utils.messages.error import (
    Conflict, 
    Server
)
from utils.messages.success import Success


class DisciplinesController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    
    def add(self, request: DisciplineRequest) -> BaseMessage:
        """
        Adiciona uma disciplina no banco de dados

        - Args:
            - request: Objeto com os dados da disciplina a ser adicionada.

        - Returns:
            - BaseMessage: Mensagem de sucesso ou erro.

        - Raises:
            - Conflict: Disciplina já existe.
            - Exception: Erro no servidor.
        """
        try:
            if discipline_exists(
                self.db_session, 
                request.name
            ):
                raise Conflict(ERROR_DISCIPLINES_ADD_CONFLICT)

            discipline = DisciplinesModel(
                id=id_generate(),
                name=request.name
            )

            self.db_session.add(discipline)
            self.db_session.commit()

            return Success(MESSAGE_DISCIPLINE_ADD_SUCCESS)
        
        except HTTPException:
            raise

        except Exception as e:
            raise Server(e)


    def get(self, discipline_name: str) -> DisciplineResponse:
        """
        Busca uma disciplina no banco de dados

        - Args:
            - name: Nome da disciplina a ser buscada.

        - Returns:
            - DisciplineResponse: Objeto com os dados da disciplina.

        - Raises:
            - NotFound: Disciplina não encontrada.
            - Exception: Erro no servidor.
        """

        discipline = get_discipline_by_name(
            self.db_session, 
            discipline_name
        )

        return self._Model_to_Response(discipline)
    

    def get_all(self) -> list[DisciplineResponse]:
        """
        Busca todas as disciplinas no banco de dados.

        - Returns:
            - List[DisciplineResponse]: Lista com os dados de todas as disciplinas.

        - Raises:
            - NotFound: Nenhuma disciplina encontrada.
            - Exception: Erro no servidor.
        """

        disciplines = get_all_disciplines(self.db_session)
        return [self._Model_to_Response(discipline) for discipline in disciplines]
    

    def update(self, name: str, request: DisciplineRequest) -> DisciplineResponse:

        """
        Atualiza uma disciplina no banco de dados

        - Args:
            - request: Objeto com os dados da disciplina a ser atualizada.

        - Returns:
            - DisciplineResponse: Objeto com os dados da disciplina.

        - Raises:
            - NotFound: Disciplina não encontrada.
            - Exception: Erro no servidor.
        """

        discipline = get_discipline_by_name(
            self.db_session, name
        )

        for key, value in request.dict().items():
            setattr(discipline, key, value)

        self.db_session.commit()

        return self._Model_to_Response(discipline)
    

    def delete(self, discipline_name: str) -> BaseMessage:
        """
        Deleta uma disciplina do sistema.

        - Args:
            - name: Nome da disciplina a ser deletada.

        - Returns:
            - BaseMessage: Mensagem de sucesso ou erro.

        - Raises:
            - NotFound: Disciplina não encontrada.
            - Exception: Erro no servidor.
        """

        discipline = get_discipline_by_name(
            self.db_session, 
            discipline_name
        )

        self.db_session.delete(discipline)
        self.db_session.commit()

        return Success(MESSAGE_DISCIPLINE_DELETE_SUCCESS)
    

    def _Model_to_Response(self, model: DisciplinesModel) -> DisciplineResponse:
        """
        Converte um modelo de disciplina para um objeto de resposta.

        - Args:
            - model: Modelo da disciplina.

        - Returns:
            - DisciplineResponse: Objeto com os dados da disciplina.
        """

        return DisciplineResponse(
            **model.dict()
        )