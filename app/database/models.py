from datetime import datetime
from sqlalchemy import (
    DateTime, 
    Float, 
    ForeignKey, 
    Integer, 
    String, 
    Text
)
from sqlalchemy.orm import Mapped, mapped_column


from os.path import abspath, dirname
import sys
sys.path.append(dirname(abspath(__file__))) #Garantindo a criação das tabelas


from base import Base
from connection import engine


class UserModel(Base):
    """
    - cpf: str
    - name: str
    - phone: str
    - phone_optional: str | None
    - email: str
    - password: str
    - level: str    
    """

    __tablename__ = 'user'  
    
    cpf: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_optional: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique= False, nullable=False)
    level: Mapped[int] = mapped_column(Integer, unique=False ,nullable=False)


class WarningModel(Base):
    """
    - id: str
    - parent_cpf: str
    - text: str
    - file_path: str | None
    - date: datetime
    """

    __tablename__ = 'warning'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    parent_cpf: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class ChildModel(Base):
    """
    - cpf: str
    - name: str
    - matriculation: str
    """
    __tablename__ = 'child'

    cpf: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    matriculation: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class NotifyModel(Base):
    """
    -id: str
    - text: str
    - date: datetime
    - origin: str
    - parent_cpf: str
    - child_cpf: str
    """
    __tablename__ = 'notify'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    origin: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"),nullable=False)
    parent_cpf: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"), nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), nullable=False)


class ChildParentsModel(Base):
    """
    - id: str
    - child_cpf: str
    - parent_cpf: str
    """
    __tablename__ = 'child_parents'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), primary_key=True)
    parent_cpf: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"), primary_key=True)

class ClassModel(Base):
    """
    - id: str
    - name: str
    - room: str
    - teacher_cpf: str
    """
    __tablename__ = 'class'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    room: Mapped[str] = mapped_column(String, nullable=False)
    teacher_cpf: Mapped[str] = mapped_column(String, ForeignKey("user.cpf"), nullable=False)


class ClassEventModel(Base):
    """
    - id: str
    - class_id: str
    - start_date: datetime
    - end_date: datetime
    """
    __tablename__ = 'class_event'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("class.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class ClassStudantModel(Base):
    """
    - id: str
    - class_id: str
    - child_cpf: str
    """

    __tablename__ = 'class_studant'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("class.id"), nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), nullable=False)


class PresenceModel(Base):
    """
    - id: str
    - class_event_id: str
    - child_cpf: str
    - type: str
    - date: datetime
    """
    __tablename__ = 'presence'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_event_id: Mapped[str] = mapped_column(String, ForeignKey("class_event.id"), nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # P or F
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class NoteModel(Base):
    """
    - id: str
    - class_event_id: str
    - points: float
    - child_cpf: str
    - date: datetime
    """
    __tablename__ = 'note'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_event_id: Mapped[str] = mapped_column(String, ForeignKey("class_event.id"), nullable=False)
    points: Mapped[float] = mapped_column(Float, nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)


def create_tables(engine) -> bool:
    """
    Cria no banco todas as entidades necessárias para o sistema
    """
    try:
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        print(f"Erro ao criar entidades: {e}")
        return False

if __name__ == "__main__":

    print("Starting Database")
    success = create_tables(engine)
    print(f"Database setup {'succeeded' if success else 'failed'}")