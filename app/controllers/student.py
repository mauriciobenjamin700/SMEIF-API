from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


from constants.child import (
    ERROR_CHILD_ADD_CONFLICT_FIELD_CPF,
    ERROR_CHILD_ADD_NOT_FOUND_PARENT,
    ERROR_CHILD_ADD_PARENT_ALREADY_ASSOCIATE_PARENT,
    ERROR_CHILD_ADD_PARENT_LIMIT_REACHED,
    ERROR_CHILD_CHANGE_CLASS_STUDENT_ALREADY_ASSOCIATE,
    ERROR_CHILD_DELETE_PARENT_LIMIT_REACHED,
    ERROR_CHILD_DELETE_PARENT_NOT_ASSOCIATE_PARENT,
    ERROR_CHILD_GET_NOT_FOUND,
    ERROR_CHILD_INVALID_FIELD_KINSHIP,
    MAX_PARENT,
    MESSAGE_CHILD_ASSOCIATE_PARENT_SUCCESS,
    MESSAGE_CHILD_DELETE_PARENT_SUCCESS,
    MESSAGE_CHILD_DELETE_SUCCESS,
    MIN_PARENT
)
from database.queries.existence import(
    child_exists,
    parent_exists
)
from database.queries.get import (
    get_child_by_cpf,
    get_class_by_id, get_class_student_by_child_cpf
)
from database.queries.get_all import get_all_children
from database.mapping.student import (
    map_ChildModel_to_StudentResponse,
    map_StudentRequest_to_ChildModel
)
from database.models import(
    ChildParentsModel,
    ClassStudentModel
)
from schemas.base import BaseMessage, Kinship
from schemas.child import(
    ChildRequest,
    StudentRequest,
    StudentResponse
)
from services.generator.ids import id_generate
from utils.format import (
    unformat_cpf, 
    unformat_date
)
from utils.messages.error import(
    Conflict,
    NotFound,
    Server,
    UnprocessableEntity
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
                unformat_cpf(cpf)
            )

            class_ = child.class_student.class_

            return map_ChildModel_to_StudentResponse(
                self.db_session,
                child,
                class_
            )
        
        except HTTPException:

            raise

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
                        child,
                        class_
                    )
                )

            return students
        
        except HTTPException:

            raise 

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
                unformat_cpf(request.cpf)
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
                child,
                child.class_student.class_
            )

            self.db_session.commit()

            return response
        
        except HTTPException:

            raise

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
                unformat_cpf(cpf)
            )

            self.db_session.delete(child)

            self.db_session.commit()

            return Success(MESSAGE_CHILD_DELETE_SUCCESS)
        
        except HTTPException:

            raise

        except Exception as e:

            raise Server(e)
        
    #TODO: Testar todas as funcs a baixo
    def change_class(self, student_cpf: str, to_class_id: str, is_transfer: bool = True) -> StudentResponse:
        """
        Troca a turma de um estudante.

        - Args:
            - student_cpf: CPF do estudante.
            - to_class_id: ID da turma para onde o estudante será movido.
            - is_transfer: Indica se a mudança de turma é uma transferência ou Alocação de um aluno sem turma a uma turma (True em caso de transferência e False em caso de Alocação de aluno parado).

        - Returns:
            - Objeto com os dados do estudante atualizado.
        """

        try:

            child = get_child_by_cpf(
                self.db_session, 
                unformat_cpf(student_cpf)
            )

            class_ = get_class_by_id(self.db_session, to_class_id)


            if is_transfer:

                class_student = get_class_student_by_child_cpf(
                    self.db_session,
                    student_cpf
                )

                if class_student.class_id == class_.id: # conferindo se o aluno já está na turma
                    
                    raise Conflict(ERROR_CHILD_CHANGE_CLASS_STUDENT_ALREADY_ASSOCIATE)

                class_student = to_class_id
                
            else:

                class_student = ClassStudentModel(
                    id = id_generate(),
                    class_id = to_class_id,
                    child_cpf=student_cpf
                )

                self.db_session.add(class_student)

            self.db_session.commit()

            response = map_ChildModel_to_StudentResponse(
                self.db_session,
                child,
                class_
            )

            return response
        
        except HTTPException:

            raise

        except Exception as e:

            raise Server(e)

    def add_parent(self, child_cpf: str, kinship: str, parent_cpf: str) -> BaseMessage:
        """
        Adiciona um responsável para um estudante

        - Args:
            - child_cpf: CPF do estudante.
            - kinship: Parentesco do responsável.
            - parent_cpf: CPF do responsável.

        - Returns:
            - Mensagem de sucesso.


        - Raises:
            - UnprocessableEntity: Caso o parentesco seja inválido.
            - NotFound: Caso o responsável do estudante não seja encontrado.
            - NotFound: Caso o estudante não seja encontrado.
            - Conflict: Caso o responsável já esteja associado ao estudante.
            - Server: Caso ocorra algum erro no servidor.
        """
        try:

            if kinship not in Kinship.__dict__.values():
                raise UnprocessableEntity(ERROR_CHILD_INVALID_FIELD_KINSHIP)
            

            if not parent_exists(self.db_session, parent_cpf):
                raise NotFound(ERROR_CHILD_ADD_NOT_FOUND_PARENT)
            
            if not child_exists(self.db_session, child_cpf):
                raise NotFound(ERROR_CHILD_GET_NOT_FOUND)

            associations = self.db_session.scalars(
                select(ChildParentsModel).where(
                    ChildParentsModel.child_cpf == child_cpf
                )
            ).all()

            for association in associations:
                if association.parent_cpf == parent_cpf:
                    raise Conflict(ERROR_CHILD_ADD_PARENT_ALREADY_ASSOCIATE_PARENT)
                
            if len(associations) == MAX_PARENT:
                raise Conflict(ERROR_CHILD_ADD_PARENT_LIMIT_REACHED)

            child_parent = ChildParentsModel(
                id=id_generate(),
                kinship=kinship,
                child_cpf=child_cpf,
                parent_cpf=parent_cpf
            )

            self.db_session.add(child_parent)
            self.db_session.commit()

            return Success(MESSAGE_CHILD_ASSOCIATE_PARENT_SUCCESS)
        
        except HTTPException:
                
                raise

        except Exception as e:

            raise Server(e)

    def delete_parent(self, child_cpf: str, parent_cpf: str) -> BaseMessage:
        """
        Desvincula um responsável de um estudante

        - Args:
            - child_cpf: CPF do estudante.
            - parent_cpf: CPF do responsável.
        
        - Returns:
            - Mensagem de sucesso.

        - Raises:
            - NotFound: Caso o responsável do estudante não seja encontrado.
            - NotFound: Caso o estudante não seja encontrado.
            - Conflict: Caso o responsável não esteja associado ao estudante.
            - Server: Caso ocorra algum erro no servidor.
        """

        try:

            if not parent_exists(self.db_session, parent_cpf):
                raise NotFound(ERROR_CHILD_ADD_NOT_FOUND_PARENT)
            
            if not child_exists(self.db_session, child_cpf):
                raise NotFound(ERROR_CHILD_GET_NOT_FOUND)

            associations = self.db_session.scalars(
                select(ChildParentsModel).where(
                    ChildParentsModel.child_cpf == child_cpf
                    )
                ).all()

            if len(associations) == MIN_PARENT:
                raise Conflict(ERROR_CHILD_DELETE_PARENT_LIMIT_REACHED)

            child_parent = None
            
            for association in associations:
                if association.parent_cpf == parent_cpf:
                    child_parent = association
                    break

            if child_parent is None:
                raise NotFound(ERROR_CHILD_DELETE_PARENT_NOT_ASSOCIATE_PARENT)

            self.db_session.delete(child_parent)
            self.db_session.commit()

            return Success(MESSAGE_CHILD_DELETE_PARENT_SUCCESS)
        

        except HTTPException:
                
                raise
        
        except Exception as e:

            raise Server(e)