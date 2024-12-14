from abc import ABC, abstractclassmethod
from typing import Any

class PersistenceBase(ABC):

    @abstractclassmethod
    def save():
        pass

    @abstractclassmethod
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
