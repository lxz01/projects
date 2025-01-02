"""
存储文件类型
"""
import atexit


class File:
    """
    所有文件基类
    """
    types: list[type] = []  # 记录所有继承此类的子类
    _start_functions: list = []  # 记录所有使用第一次使用对象(装饰器)的方法
    _used_functions: list = []  # 记录所有使用每次使用(装饰器)的方法(除去第一次和最后一次使用)
    _end_functions: list = []  # 记录所有使用结束(装饰器)的方法
    def __init_subclass__(cls):
        """
        所有子类初始化时, 添加到types中
        """
        cls.types.append(cls)

    def judgment(self) -> bool:
        """
        子类需继承
        判断是否为该类型
        """
        return True

    # 装饰器方法
    def used(self):
        """
        装饰器方法
        当对象使用时调用
        """
        def wrapper(func):
            def inner(*args, **kwargs):
                self._used_functions.append(func)
                return func(*args, **kwargs)
            return inner
        return wrapper

    def start(self):
        """
        装饰器方法
        当对象第一次使用时调用
        """
        def wrapper(func):
            def inner(*args, **kwargs):
                self.first()
                return func(*args, **kwargs)
            return inner
    
    def end(self):
        """
        装饰器方法
        当程序结束时调用
        """
        def wrapper(func):
            def inner(*args, **kwargs):
                atexit.register(func)
                self._end_functions.append(func)
                return func(*args, **kwargs)
            return inner
        return wrapper


