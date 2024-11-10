from datetime import datetime
from sqlalchemy import (
    CHAR,
    DateTime, 
    Float, 
    ForeignKey, 
    Integer, 
    String, 
    Text
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
    - cpf: str
    - name: str
    - phone: str
    - phone_optional: str | None
    - email: str
    - password: str
    - level: str

    relationships:
    - address: AddressModel
    - child_parents: list[ChildParentsModel]
    """

    __tablename__ = 'user'  
    
    cpf: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_optional: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique= False, nullable=False)
    level: Mapped[int] = mapped_column(Integer, unique=False ,nullable=False)
    address_id: Mapped[str] = mapped_column(String, ForeignKey("address.id"), nullable=False)

    address = relationship(
        "AddressModel", 
        back_populates="users",
        uselist=False
    )
    child_parents = relationship(
        "ChildParentModel",
        back_populates="parent",
        uselist=True
    )



class AddressModel(BaseModel):
    """
    - id: str
    - state: str
    - city: str
    - neighborhood: str
    - street: str
    - house_number: str
    - complement: str | None

    relationships:
    - users: list[UserModel]
    - children: list[ChildModel]
    """

    __tablename__ = 'address'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    state: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    neighborhood: Mapped[str] = mapped_column(String, nullable=False)
    street: Mapped[str] = mapped_column(String, nullable=False)
    house_number: Mapped[str] = mapped_column(String, nullable=False)
    complement: Mapped[str] = mapped_column(String, nullable=True)

    users = relationship(
        "UserModel",
        back_populates="address",
        uselist=True,
        order_by="UserModel.name"
    )
    children = relationship(
        "ChildModel",
        back_populates="address",
        uselist=True,
        order_by="ChildModel.name"
    )

class WarningModel(BaseModel):
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


class ChildModel(BaseModel):
    """
    - matriculation: str
    - cpf: str
    - name: str
    - birth_date: datetime
    - gender: str
    - address_id: str
    - dependencies: str | None

    relationships:
    - address: AddressModel
    - child_parents: list[ChildParentsModel]
    """
    __tablename__ = 'child'

    matriculation: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    cpf: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    gender: Mapped[str] = mapped_column(CHAR, unique=False,nullable=False)
    address_id: Mapped[str] = mapped_column(String, ForeignKey("address.id"), nullable=False)
    dependencies: Mapped[str] = mapped_column(Text, unique=False, nullable=True)

    address = relationship(
        "AddressModel",
        back_populates="children",
        uselist=False
    )
    child_parents = relationship(
        "ChildParentsModel",
        back_populates="child",
        uselist=True
    )


class ChildParentsModel(BaseModel):
    """
    - id: str
    - kindship: str
    - child_cpf: str
    - parent_cpf: str

    relationships:
    - child: list[ChildModel]
    - parent: list[UserModel]
    """
    __tablename__ = 'child_parents'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    kindship: Mapped[str] = mapped_column(String, unique=False,nullable=False)
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
    - id: str
    - grade_level: int
    - room: str
    """
    __tablename__ = 'class'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    grade_level: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    room: Mapped[str] = mapped_column(String, unique=False,nullable=False)




class ClassStudantModel(BaseModel):
    """
    - id: str
    - class_id: str
    - child_cpf: str
    """

    __tablename__ = 'class_studant'

    id: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("class.id"), nullable=False)
    child_cpf: Mapped[str] = mapped_column(String, ForeignKey("child.cpf"), nullable=False)



class PresenceModel(BaseModel):
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


class NoteModel(BaseModel):
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


def create_tables():
    """
    Cria no banco todas as entidades necessárias para o sistema
    """
    try:
        BaseModel.metadata.create_all(engine)
        print("Starting Database")
    except Exception as e:
        print(f"Erro ao criar entidades: {e}")