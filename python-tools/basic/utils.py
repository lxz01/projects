from typing import Any, Callable, Iterable
from basic.persistence.base import PersistenceBase
__all__ = [
    "Null", "Out", "ListPlus", "DictPlus"
]


class Null:

    def __getitem__(self, __key: Any):
        return Null()

    def __getattribute__(self, __name: str) -> Any:
        return Null()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
    
    def __repr__(self) -> str:
        return "null"

    def __str__(self) -> str:
        return "null"


class Out:
    """
    输出类
    """
    title: str = ""

    @classmethod
    def print(cls, *args, end: str = "\n", seq: str = None):
        # print(args)
        _a = []
        for arg in args:
            if isinstance(arg, dict):
                for _k, _v in arg.items():
                    _a.append(_k)
                    _a.append(_v)
            elif isinstance(arg, list):
                _a.extend(arg)
            else:
                _a.append(arg)
        args = _a
        if len(args) == 1:
            print(cls.title+str(args[0]), end=end)
            return
        elif len(args) == 0:
            print(cls.title, end=end)
        elif len(args) == 2:
            if seq is None:
                seq = [":"]
        else:
            if seq is None:
                seq = [", "]
        __ = str()
        for _ in range(len(args)):
            _s = seq[_] if len(seq) > _ else seq[-1]
            if _ + 1 == len(args):
                __ += str(args[_])
                continue
            __ += str(args[_]) + str(_s)
        print(cls.title+str(__), end=end)


class DictPlus(dict):
    """
    dict的继承类
    """

    def __getitem__(self, __key: Any) -> Any:
        if __key not in self.keys():
            return Null()
        return super().__getitem__(__key)
    
    def __getattribute__(self, key: str):
        try:
            # 尝试直接获取属性
            return super().__getattribute__(key)
        except AttributeError:
            # 如果属性不存在，尝试作为字典键获取
            if key in self:
                return self[key]
            else:
                return Null()

    def __setattr__(self, __name: str, __value: Any) -> None:
        self[__name] = __value
        return super().__setattr__(__name, __value)

    def foreach(self, function: Callable[[object, object], list[object]]):
        """
        循环遍历此对象, 运行方法
        """
        _r: list[object] = list()  # 返回值列表
        for _k, _v in self.items():
            _r.append(function(_k, _v))
        return _r

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        return self

    def deal(self, func: Callable[[object], PersistenceBase]):
        """
        整个字典放到函数中运行
        """
        return func(self)


class ListPlus(list):

    def foreach(self, function: Callable[[object, None|int], list[object]]):
        """
        循环遍历此对象, 运行方法
        """
        _r: list[object] = list()
        for _ in range(len(self)):
            try:
                _r.append(function(self[_], _))
            except TypeError:
                _r.append(function(self[_], None))
        return _r
    
    def extend(self, __iterable: Iterable) -> None:
        super().extend(__iterable)
        return self


"""
存储一些基本工具
1.自定义的Null类
2.DictPlus: 增强版的dict
3.ListPlus: 增强版的list
4.Out: 输出类, 存储的都是各种各样的输出方法
"""