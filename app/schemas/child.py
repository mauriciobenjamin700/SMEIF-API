from pydantic import Field


from schemas.address import Address
from schemas.base import BaseSchema



class StudentRequest(BaseSchema):
    """
    - name: str
    - birth_date: str
    - cpf: str
    - gender: str


    """

    cpf: str = Field(
        title="CPF",
        description="CPF do aluno",
        examples=["123.456.789-00", "987.654.321-00"]
    )
    name: str = Field(
        title="Nome",
        description="Nome do aluno",
        examples=["João", "Maria", "José"]
    )
    birth_date: str = Field(
        title="Data de Nascimento",
        description="Data de nascimento do aluno",
        examples=["1990-01-01"]
    )
    gender: str = Field(
        title="Gênero",
        description="Gênero do aluno",
        examples=["M", "F", "Z"],
    )
    class_id: str = Field(
        title="ID da Turma",
        description="Código da Turma",
        examples=['1', '2', '3']
    )
    address: Address
    kinship: str = Field(
        title="Parentesco",
        description="Parentesco do aluno com o Responsável",
        examples=["Pai", "Mãe", "Avô", "Avó", "Tio", "Tia", "Irmão", "Irmão", "Primo", "Prima", "Responsável legal", "Tutor", "Padrasto", "Madrasta", "Outros"]
    )
    parent_cpf: str = Field(
        title="CPF do Responsável",
        description="CPF do Responsável",
        examples=["123.456.789-00", "987.654.321-00"]
    )
    complement: str = Field(
        title="Necessidades especiais",
        description="Caso o aluno tenha alguma condição médica, alergia, ou necessidades de acompanhamento especial.",
        examples=["Autismo", "Intolerância a lactose", "mudo", "Cadeirante"]
    )


class StudentResponse(BaseSchema):
    """
    - matriculation: str
    - name: str
    - class_info: str
    - shift: str
    """
    matriculation: str = Field(
        title="Matrícula",
        description="Número de matrícula do aluno",
        examples=["123456", "654321"]
    )
    name: str = Field(
        title="Nome",
        description="Nome do aluno",
        examples=["João", "Maria", "José"]
    )
    class_info: str = Field(
        title="Informações da Turma",
        description="Informações da turma",
        examples=["5° Ano A", "6° Ano B", "8° Ano C"]
    )
    shift: str = Field(
        title="Turno",
        description="Turno da disciplina",
        examples=["Matutino", "Vespertino", "Noturno"]
    )