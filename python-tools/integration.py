from basic.utils import *
from basic.persistence.json import Json
from basic.persistence.yaml import Yaml
from basic.persistence.base import PersistenceBase

"""
集成功能
    1.仅当创建某个对象时, 才会导入对应的模块
    2.功能可独立, 可聚合
    3.包含基本的功能或拓展的功能
功能(basic)
    error: 基础错误包
    logging: 基础日志包, 可以替换升级
    1.utils: 工具包
        * function默认为print
        - copy(object, assemble: bool = True): 传入对象, 深拷贝; 列表字典额外判断
        - get(place: object | str | dict, key: str | re.complie | obj, default: None): 从对象中获取值, default为默认, default中的默认值可以在config中设置
                - 从对象获取值; 对象, 属性, 默认值
                - 从路径获取文件; 路径, 文件名/正则对象, 默认值
                - 从字典获取值; 字典, 键, 默认值
        - run(function): 读取config, 对方法进行拦截报错, 通过config的配置放行和重新报错或忽略
        - PythonPath: 读取和写入环境目录， 添加某个模块为pth中的python path
        - ListPlus;继承列表, 实现其他功能
            1.foreach(function(object)): 每个项运行函数
        - DictPlus;继承字典, 实现其他功能
            1.通过对象方式访问数据
            2.foreach(function(object, object)): 每个项运行函数
            3.get_key(value): 通过值获取键, 默认为第一个
            4.get_keys(value): 通过值获取键, 返回tuple
        - ConfigBase: 配置基本类, 加载路径默认为config
            * 默认都需要编译器识别
            1.读取config中的配置, 销毁对象会读取设置项是否保存, 保存位置
            2.继承此类可当做配置文件, 有以下参数
            3.参数
                - name: 默认为类名, config.py中不存在
                - path: 存储位置, 默认为./data/config/, config.py中不存在
                - reading: 是否读取, 默认为True
                - writing: 是否可以写入, 默认为False
        - plan: 计划实现; 可以定时/阻塞/线程等方式计划任务
        - multiple: 多个程序单独运行; 单独的类, 通过某个方法进行停止, ipc通信
        - initialize: 初始化
            1.判断某些文件夹是否存在, 再通过读取config额外创建文件文件夹等
    2.Realize: 实现包, 实现一些基本的控制方法
        - base: 控制基础包, 用于在控制中或后进行持久化或网络传输等
        - file: 文件控制实现, 可删除自身, 调用时导入sys
        - ssh: 远程控制实现
        - window: 窗口控制实现
        - sql: sql控制实现, mysql, sqlite, mongodb, redis
        - cmd: 控制计算机的cmd等输入输出
        - peripheral: 控制计算机外部设备
        - graphics: 图像处理, 截屏, 摄像, 录音等
        - notification: 通知处理
            1.tk.messagebox的其中三个
            2.从用户输入获取信息
            3.系统通知toast
            4.模拟系统卡片通知, 包装成一个类
        - external_command: 外部命令处理
        - file_manage_dom: 类似于dom的文件管理, 通过对象.方式访问; 纯属娱乐
"""


def demo():
    print(1)
