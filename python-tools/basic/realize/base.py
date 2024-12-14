from abc import ABC
from basic.error import LxzBaseExpection


class RealizeExpection(LxzBaseExpection):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Realize(ABC):
    """
    所有实现功能继承此类
    """