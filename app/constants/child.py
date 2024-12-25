ERROR_CHILD_REQUIRED_FIELD_CPF = "CPF do estudante é obrigatório"
ERROR_CHILD_REQUIRED_FIELD_NAME = "Nome do estudante é obrigatório"
ERROR_CHILD_REQUIRED_FIELD_BIRTH_DATE = "Data de nascimento do estudante é obrigatória"
ERROR_CHILD_REQUIRED_FIELD_GENDER = "Gênero do estudante é obrigatório"
ERROR_CHILD_REQUIRED_FIELD_CLASS_ID = "ID da turma do estudante é obrigatório"
ERROR_CHILD_REQUIRED_FIELD_KINSHIP = "Parentesco com o responsável é obrigatório"
ERROR_CHILD_REQUIRED_FIELD_PARENT_CPF = "CPF do responsável é obrigatório"
ERROR_CHUILD_REQUIRED_FIELD_STUDENT_CPF = "CPF do estudante é obrigatório"
ERROR_CHILD_INVALID_FIELD_BIRTH_DATE = "Data de nascimento do estudante inválida\n Aluno deve ser menor de idade"
ERROR_CHILD_INVALID_FIELD_KINSHIP = "Tipo de parentesco invalido"

ERROR_CHILD_ADD_CONFLICT_FIELD_CPF = "CPF do estudante já cadastrado"
ERROR_CHILD_ADD_NOT_FOUND_PARENT = "Não foi possível encontrar o responsável pelo estudante"

ERROR_CHILD_GET_NOT_FOUND = "Estudante não encontrado"
ERROR_CHILD_GET_ALL_NOT_FOUND = "Nenhum estudante encontrado"
ERROR_CHILD_GET_CLASS_STUDENT_NOT_FOUND = "Aluno não vinculado a nenhuma turma"
ERROR_CHILD_CHANGE_CLASS_STUDENT_ALREADY_ASSOCIATE = "Estudante já está matriculado na turma"
ERROR_CHILD_ADD_PARENT_ALREADY_ASSOCIATE_PARENT = "Responsável já está vinculado ao estudante"
ERROR_CHILD_DELETE_PARENT_NOT_ASSOCIATE_PARENT = "Responsável não está vinculado ao estudante"
ERROR_CHILD_ADD_PARENT_LIMIT_REACHED = "Número máximo de responsáveis atingido"
ERROR_CHILD_DELETE_PARENT_LIMIT_REACHED = "Número mínimo de responsáveis atingido"

MESSAGE_CHILD_DELETE_SUCCESS = "Estudante removido com sucesso"
MESSAGE_CHILD_ASSOCIATE_PARENT_SUCCESS = "Responsável vinculado com sucesso"
MESSAGE_CHILD_DELETE_PARENT_SUCCESS = "Responsável removido com sucesso"

MAX_PARENT = 2 # Número máximo de responsáveis por estudante
MIN_PARENT = 1 # Número mínimo de responsáveis por estudante