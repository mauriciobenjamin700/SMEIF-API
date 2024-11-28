from datetime import datetime
from sqlalchemy import (
    CHAR,
    Date,
    DateTime, 
    Float, 
    ForeignKey, 
    Integer, 
    String, 
    Text,
    Time
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship
)


from os.path import abspath, dirname
import sys
sys.path.append(dirname(abspath(__file__))) #Garantindo a criação das tabelas


from base import BaseModel
from connection import engine



class UserModel(BaseModel):
    """
    Dados de um usuário do sistema

    - cpf: str
    - name: str
    - birth_date: datetime
    - gender: str
    - phone: str
    - phone_optional: str | None
    - email: str
    - password: str
    - level: str
    - state: str
    - city: str
    - neighborhood: str
    - street: str
    - house_number: str
    - complement: str | None

    relationships:
    - child_parents: list[ChildParentsModel]
    """

    __tablename__ = 'user'  
    
    cpf: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    gender: Mapped[str] = mapped_column(CHAR(1), unique=False,nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_optional: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique= False, nullable=False)
    level: Mapped[int] = mapped_column(Integer, unique=False ,nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    neighborhood: Mapped[str] = mapped_column(String, nullable=False)
    street: Mapped[str] = mapped_column(String, nullable=False)
    house_number: Mapped[str] = mapped_column(String, nullable=False)
    complement: Mapped[str] = mapped_column(String, nullable=True)

    child_parents = relationship(
        "ChildParentsModel",
        back_populates="parent",
        uselist=True
    )

    class_teacher = relationship(
        "ClassTeacherModel",
        back_populates="user",
        uselist=True,
    )


class WarningModel(BaseModel):
    """
    Dados de avisos ou advertências

    - id: str
    - parent_cpf: str
    - theme: str
    - text: str
    - file_path: str | None
    - date: datetime
    """

    __tablename__ = 'warning'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    parent_cpf: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"), nullable=False)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class ChildModel(BaseModel):
    """
    Dados de um aluno

    - matriculation: str
    - cpf: str
    - name: str
    - birth_date: datetime
    - gender: str
    - address_id: str
    - dependencies: str | None

    relationships:
    - child_parents: list[ChildParentsModel]
    """
    __tablename__ = 'child'

    matriculation: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    cpf: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    gender: Mapped[str] = mapped_column(CHAR(1), unique=False,nullable=False)
    dependencies: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    neighborhood: Mapped[str] = mapped_column(String, nullable=False)
    street: Mapped[str] = mapped_column(String, nullable=False)
    house_number: Mapped[str] = mapped_column(String, nullable=False)
    complement: Mapped[str] = mapped_column(String, nullable=True)

    child_parents = relationship(
        "ChildParentsModel",
        back_populates="child",
        uselist=True
    )


class ChildParentsModel(BaseModel):
    """
    Relação entre responsável legal e aluno

    - id: str
    - kinship: str
    - child_cpf: str
    - parent_cpf: str

    relationships:
    - child: list[ChildModel]
    - parent: list[UserModel]
    """
    __tablename__ = 'child_parents'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    kinship: Mapped[str] = mapped_column(String, unique=False,nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), primary_key=True)
    parent_cpf: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"), primary_key=True)

    child = relationship(
        "ChildModel",
        back_populates="child_parents",
        uselist=True,
        order_by="ChildModel.name"
    )
    parent = relationship(
        "UserModel",
        back_populates="child_parents",
        uselist=True,
        order_by="UserModel.name"
    )


class ClassModel(BaseModel):
    """
    Dados de uma turma

    - id: str
    - education_level: str
    - name: str
    - section: str
    - shift: str
    - max_students: int
    """
    __tablename__ = 'class'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    education_level: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    section: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    shift: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    max_students: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)


class ClassStudentModel(BaseModel):
    """
    Relação entre turma e aluno

    - id: str
    - class_id: str
    - child_cpf: str
    """

    __tablename__ = 'class_Student'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("class.id"), nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), nullable=False)


class DisciplinesModel(BaseModel):
    """
    Dados de uma disciplina

    - id: str
    - name: str
    """
    __tablename__ = 'disciplines'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    class_event = relationship(
        "ClassEventModel",
        back_populates="discipline",
        foreign_keys="[ClassEventModel.discipline_id]",
        uselist=True,
        cascade="all, delete-orphan"
    )


class ClassTeacherModel(BaseModel):
    """
    Relação entre turma e professor

    ### Atributes

    - id: str
    - user_cpf: str
    - class_id: str

    ### relationships:

    - class_event: list[ClassEventModel]
    """
    __tablename__ = 'class_teacher'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    user_cpf: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"), nullable=False)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("class.id"), nullable=False)

    class_event = relationship(
        "ClassEventModel", 
        back_populates="teacher", 
        foreign_keys="[ClassEventModel.teacher_id]",
        uselist=True
    )

    user = relationship(
        "UserModel",
        back_populates="class_teacher",
        foreign_keys="[ClassTeacherModel.user_cpf]",
        uselist=False
    )


class ClassEventModel(BaseModel):
    """
    Dados de aulas de uma determinada disciplina que acontecerão em uma turma

    ### Attributes:

    - id: str
    - class_id: str
    - discipline_id: str
    - teacher_id: str
    - start_date: datetime
    - end_date: datetime

    ### Relationships:

    - teacher: ClassTeacherModel

    """
    __tablename__ = 'class_event'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("class.id"), nullable=False)
    discipline_id: Mapped[str] = mapped_column(String, ForeignKey("disciplines.id"), nullable=False)
    teacher_id: Mapped[str] = mapped_column(String, ForeignKey("class_teacher.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    teacher = relationship(
        "ClassTeacherModel",
        back_populates="class_event",
        foreign_keys="[ClassEventModel.teacher_id]",
        uselist=False
    )

    discipline = relationship(
        "DisciplinesModel",
        back_populates="class_event",
        foreign_keys="[ClassEventModel.discipline_id]",
        uselist=False
    )

    recurrences = relationship(
        "RecurrencesModel",
        back_populates="class_event",
        foreign_keys="[RecurrencesModel.class_event_id]",
        uselist=True,
        cascade="all, delete-orphan"
    )


class RecurrencesModel(BaseModel):
    """
    Dados de recorrência de uma aula

    ### Attributes:

    - id: str
    - class_event_id: str
    - day_of_week: str
    - start_time: datetime
    - end_time: datetime

    ### Relationships:

    - class_event: ClassEventModel

    
    """
    __tablename__ = 'recurrences'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_event_id: Mapped[str] = mapped_column(String, ForeignKey("class_event.id", ondelete="CASCADE"), nullable=False)
    day_of_week: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[str] = mapped_column(Time, nullable=False)
    end_time: Mapped[str] = mapped_column(Time, nullable=False)

    class_event = relationship(
        "ClassEventModel",
        back_populates="recurrences",
        foreign_keys="[RecurrencesModel.class_event_id]",
        uselist=False
    )
    

class TeacherDisciplinesModel(BaseModel):
    """
    Relação entre professor e disciplina

    - id: str
    - discipline_id: str
    - teacher_cpf: str
    """
    __tablename__ = 'teacher_disciplines'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    discipline_id: Mapped[str] = mapped_column(String, ForeignKey("disciplines.id"), nullable=False)
    teacher_cpf: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"), nullable=False)


class PresenceModel(BaseModel):
    """
    Dados de presença de um aluno em uma aula

    - id: str
    - class_event_id: str
    - child_cpf: str
    - type: str
    - start_class: datetime
    - end_class: datetime
    """
    __tablename__ = 'presence'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_event_id: Mapped[str] = mapped_column(String, ForeignKey("class_event.id"), nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), nullable=False)
    type: Mapped[str] = mapped_column(CHAR(1), nullable=False) # P or F
    start_class: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_class: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class NoteModel(BaseModel):
    """
    Dados de notas de um aluno em uma determinada disciplina que acontecerá em uma turma
    
    - id: str
    - points: float
    - discipline_id: str
    - class_id: str
    - points: float
    - child_cpf: str
    """
    __tablename__ = 'note'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    points: Mapped[float] = mapped_column(Float, nullable=False)
    discipline_id: Mapped[str] = mapped_column(String, ForeignKey("disciplines.id"), nullable=False)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("class.id"), nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), nullable=False)


def create_tables():
    """
    Cria no banco todas as entidades necessárias para o sistema
    """
    try:
        BaseModel.metadata.create_all(engine)
        print("Starting Database")
    except Exception as e:
        print(f"Erro ao criar entidades: {e}")