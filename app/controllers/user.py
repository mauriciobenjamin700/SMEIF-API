from sqlalchemy.orm import Session


from controllers.base import Repository


class UserUseCases(Repository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, UserRequest) -> None:
        self.repository.add(UserRequest)

    def get(self, id) -> object:
        return self.repository.get(id)

    def get_all(self) -> list[object]:
        return self.repository.get_all()

    def update(self, id, **kwargs: object) -> None:
        self.repository.update(id, **kwargs)

    def delete(self, id) -> None:
        self.repository.delete(id)