"""
存储文件类型
"""


class File:
    """
    所有文件基类
    """
    types: list[type] = []  # 记录所有继承此类的子类
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

    def creating(self) -> None:
        """
        子类需继承
        当对象刚创建时默认调用
        """
        return None

    def using(self) -> None:
        """
        子类需继承
        当对象每次使用时默认调用
        """
        return None

    def first(self) -> None:
        """
        子类需继承
        当对象第一次使用时默认调用
        """
        return None

    # 装饰器方法
    def used(self):
        """
        装饰器方法
        当对象使用时调用
        """
        def wrapper(func):
            def inner(*args, **kwargs):
                self.using()
                return func(*args, **kwargs)
            return inner
        return wrapper

    def once(self):
        """
        装饰器方法
        当对象第一次使用时调用
        """
        def wrapper(func):
            def inner(*args, **kwargs):
                self.first()
                return func(*args, **kwargs)
            return inner


