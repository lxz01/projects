from .json import Json
from .yaml import Yaml
__all__ = ["Json", "Yaml"]
"""
对象持久化或数据存储包
1.base: 存储多种持久化的共同接口
2.json: 保存为json
3.yaml: 保存为yaml
"""