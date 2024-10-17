from abc import ABC, abstractmethod


class Repository(ABC):
    
    @abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get(self, id) -> object:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> list[object]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, id, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id) -> None:
        raise NotImplementedError