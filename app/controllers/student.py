from fastapi import HTTPException
from sqlalchemy.orm import Session


from constants.child import (
    ERROR_CHILD_ADD_CONFLICT_FIELD_CPF,
    ERROR_CHILD_ADD_NOT_FOUND_PARENT,
    MESSAGE_CHILD_DELETE_SUCCESS
)
from database.queries.existence import(
    child_exists,
    parent_exists
)
from database.queries.get import get_child_by_cpf
from database.queries.get_all import get_all_children
from database.mapping.student import (
    map_ChildModel_to_StudentResponse,
    map_StudentRequest_to_ChildModel
)
from database.models import(
    ChildParentsModel,
    ClassStudentModel
)
from schemas.base import BaseMessage
from schemas.child import(
    ChildRequest,
    StudentRequest,
    StudentResponse
)
from services.generator.ids import id_generate
from utils.format import unformat_date
from utils.messages.error import(
    Conflict,
    NotFound,
    Server
)
from utils.messages.success import Success

class StudentController:

    def __init__(self, db_session: Session):
        self.db_session = db_session


    def add(self, request: StudentRequest) -> StudentResponse:
        """
        Cadastra um estudante no sistema, adicionando o mesmo a uma turma e o vinculando a um responsável.

        - Args:
            - request: Objeto com os dados do estudante a ser cadastrado.

        - Returns:
            - Objeto com os dados do estudante cadastrado

        - Raises:
            - Conflict: Caso o CPF do estudante já exista no sistema.
            - NotFound: Caso o responsável do estudante não seja encontrado.
            - NotFound: Caso a turma do estudante não seja encontrada.

            - Server: Caso ocorra algum erro no servidor.
        """

        try:
        
            if child_exists(self.db_session, request.cpf):
                raise Conflict(ERROR_CHILD_ADD_CONFLICT_FIELD_CPF)
            
            if not parent_exists(self.db_session, request.parent_cpf):
                raise NotFound(ERROR_CHILD_ADD_NOT_FOUND_PARENT)
            
            child = map_StudentRequest_to_ChildModel(request)

            self.db_session.add(child)

            class_student = ClassStudentModel(
                id = id_generate(),
                class_id = request.class_id,
                child_cpf=request.cpf
            )

            self.db_session.add(class_student)

            child_parents = ChildParentsModel(
                id=id_generate(),
                kinship=request.kinship,
                child_cpf=request.cpf,
                parent_cpf=request.parent_cpf
            )

            self.db_session.add(child_parents)

            response =  map_ChildModel_to_StudentResponse(
                self.db_session,
                child,
                request.class_id
            )

            self.db_session.commit()

            return response


        except HTTPException:

            raise

        except Exception as e:

            raise Server(e)


    def get(self, cpf: str) -> StudentResponse:
        """
        Busca um estudante no sistema.

        - Args:
            - cpf: CPF do estudante a ser buscado.

        - Returns:
            - Objeto com os dados do estudante buscado.

        - Raises:
            - NotFound: Estudante não encontrado.
            - NotFound: Turma não encontrada.
            - Server: Caso ocorra algum erro no servidor.
        """

        try:

            child = get_child_by_cpf(
                self.db_session, 
                cpf
            )

            class_ = child.class_student.class_

            return map_ChildModel_to_StudentResponse(
                self.db_session,
                class_
            )

        except Exception as e:

            raise Server(e)
        

    def get_all(self) -> list[StudentResponse]:
        """
        Busca todos os estudantes cadastrados no sistema.

        - Returns:
            - Lista com objetos contendo os dados de todos os estudantes cadastrados.

        - Raises:
            - NotFound: Turma não encontrada.
            - NotFound: Estudantes não encontrados.
            - Server: Caso ocorra algum erro no servidor.
        """

        try:

            children = get_all_children(self.db_session)

            students = []

            for child in children:

                class_ = child.class_student.class_

                students.append(
                    map_ChildModel_to_StudentResponse(
                        self.db_session,
                        class_
                    )
                )

            return students

        except Exception as e:

            raise Server(e)
        

    def update(self, request: ChildRequest) -> StudentResponse:
        """
        Atualiza os dados de um estudante no sistema.

        - Args:
            - cpf: CPF do estudante a ser atualizado.
            - request: Objeto com os novos dados do estudante.

        - Returns:
            - Objeto com os dados do estudante atualizado.

        - Raises:
            - NotFound: Estudante não encontrado.
            - NotFound: Turma não encontrada.
            - Server: Caso ocorra algum erro no servidor.
        """

        try:

            child = get_child_by_cpf(
                self.db_session, 
                request.cpf
            )

            for key, value in request.dict().items():
                if key == "birth_date":
                    value = unformat_date(value, False)
                    setattr(child, key, value)

                elif key == "Address":
                    for address_key, address_value in value.dict().items():
                        setattr(child, address_key, address_value)
                else:
                    setattr(child, key, value)

            response = map_ChildModel_to_StudentResponse(
                self.db_session,
                child.class_student.class_
            )

            self.db_session.commit()

            return response

        except Exception as e:

            raise Server(e)


    def delete(self, cpf: str) -> BaseMessage:
        """
        Deleta um estudante do sistema.

        - Args:
            - cpf: CPF do estudante a ser deletado.

        - Returns:
            - Mensagem de sucesso.
        """

        try:

            child = get_child_by_cpf(
                self.db_session, 
                cpf
            )

            self.db_session.delete(child)

            self.db_session.commit()

            return Success(MESSAGE_CHILD_DELETE_SUCCESS)

        except Exception as e:

            raise Server(e)
        
    
    def change_class(self):
        pass

    def add_parent(self):
        pass

    def remove_parent(self):
        pass