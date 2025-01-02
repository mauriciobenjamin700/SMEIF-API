from datetime import datetime


from schemas.base import BaseSchema


class WarningRequest(BaseSchema):
    """
    - parent_cpf: str
    - theme: str
    - text: str
    """
    parent_cpf: str
    theme: str
    text: str


class WarningDB(WarningRequest):
    """
    - id: str
    - file_path: str | None
    - date: datetime
    - parent_cpf: str
    - theme: str
    - text: str
    """
    id: str
    file_path: str | None
    date: datetime