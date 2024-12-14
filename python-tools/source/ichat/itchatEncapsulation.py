# itchat的封装
import abc
import os
import threading
import time
from enum import Enum

# __all__ = [
#     "ItchatLxzException", "ImgStatus",
#     "MessageType", "Message", "Friend",
#     "Group", "mts"
# ]

from types import MethodType
from typing import Callable

from source.ichat.itchat import Core
from source.ichat.itchat.storage import Queue


class ItchatLxzException(Exception):
    # 拦截所有本模块的错误
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class ImgStatus(Enum):
    pic = 2  # 是否为图片
    other = 1  # 为其他类型


class MessageType:
    # 消息类型
    id: int  # 消息类型id
    name: str  # 消息类型名称

    cls_msssage_types: list["MessageType"]

    def __init__(self, _id: int, name: str):
        """
        初始化
        :param _id: id
        :param name: name
        """
        self.id = _id
        self.name = name

    @classmethod
    def of(cls, id_or_name: int | str):
        """
        通过id或者name获取消息类型
        :param id_or_name: id或者name
        :return: MessageType
        """
        if isinstance(id_or_name, int):
            for _t in cls.cls_msssage_types:
                if id_or_name == _t.id:
                    return _t
            raise ItchatLxzException(f"未找到对应id对应的消息类型({id_or_name})")
        else:
            for _t in cls.cls_msssage_types:
                if id_or_name == _t.name:
                    return _t
            raise ItchatLxzException(f"未找到对应name对应的消息类型({id_or_name})")


class Friend:
    md5: str  # 微信号哈希
    nickname: str  # 昵称
    headimg: str  # 头像地址
    remark: str  # 备注
    sex: str  # 性别
    signature: str  # 个性标签
    province: str = "None"  # 省份
    city: str = "None"  # 城市
    star: bool  # 星标

    friends: list["Friend"]  # 优先接受类属性friends

    @classmethod
    def of(cls, /, _id: str = None, _nickname: str = None):
        """
        根据id或昵称获取对象
        :param _id: id
        :param _nickname: nickname
        :return:
        """
        if (_id is None) and (_nickname is None):
            return cls.friends[0]  # 返回自身
        elif _nickname is None:
            for _f in cls.friends:
                if _f.md5 == _id:
                    return _f
            return cls.friends[0]
        else:
            for _f in cls.friends:
                if _f.nickname == _nickname:
                    return _f
            return cls.friends[0]

    def loading(self, msg: dict):
        """
        通过msg加载信息
        :param msg: 消息
        :return: self
        """
        _f = Friend()
        _f.md5 = msg["UserName"] if "UserName" in msg else None
        _f.nickname = msg["NickName"] if "NickName" in msg else None
        _f.headimg = msg["HeadImgUrl"] if "HeadImgUrl" in msg else None
        _f.remark = msg["RemarkName"] if "RemarkName" in msg else None
        _f.signature = msg["Signature"] if "Signature" in msg else None
        _f.star = msg["StarFriend"] if "StarFriend" in msg else False
        _f.province = msg["Province"] if "Province" in msg else None
        _f.city = msg["City"] if "City" in msg else None
        if msg["Sex"] == 1:
            _f.sex = "男"
        elif msg["Sex"] == 0:
            _f.sex = "女"
        else:
            _f.sex = "未知"
        self = _f
        return self

    def __repr__(self):
        return self.nickname + "|" + self.md5 + "|" + self.sex + "|" + self.remark

    def __str__(self):
        return self.__repr__()


class Group:
    """
    群聊
    """
    md5: str  # 群聊哈希
    nickname: str  # 群名
    groups: list["Group"]  # 优先接受类属性of使用

    def __init__(self, _id: int = None, _nickname: str = None):
        self.id = _id
        self.nickname = _nickname

    def loading(self, msg: dict):
        """
        通过消息加载信息
        :param msg: 消息
        :return: self
        """
        self.nickname = msg["NickName"]
        self.md5 = msg["UserName"]
        return self

    @classmethod
    def of(cls, /, _id: str = None, _nickname: str = None):
        """
        根据id或昵称获取对象
        :param _id: id
        :param _nickname: name
        :return:
        """
        if (_id is None) and (_nickname is None):
            return Group("null", "null")
        elif _nickname is None:
            for _f in cls.groups:
                if _f.md5 == _id:
                    return _f
            return Group("null", "null")
        else:
            for _f in cls.groups:
                if _f.nickname == _nickname:
                    return _f
            return Group("null", "null")


class Message:
    id: str  # 消息的id
    fromUserName: str  # 消息来源用户
    toUserName: str  # 消息目标用户
    msgType: MessageType  # 消息类型
    content: str  # 消息
    timestamp: int  # 消息时间戳
    voiceLength: int  # 语音时长, 毫秒
    fileName: str  # 当为文件或图片时
    mediaId: str  # 文件下载路径

    # 群聊专有msg信息
    chatroom: bool  # 是否为群聊
    actualUserName: str  # 当前发消息的用户id
    actualNickName: str  # 当前发消息的用户昵称

    friends: list[Friend]  # 所有用户, 类属性
    groups: list[Group]  # 所有群组, 类属性
    messageTypes: list[MessageType]  # 类型

    def __init__(self, msg: dict):
        """
        处理消息演变为本类的对象
        :param msg: dict网络接收的信息流
        """
        self.msg = msg
        if "MsgId" not in msg:
            self.id = "system"
            self.content = msg["Content"]
        else:
            self.id = msg["MsgId"] if "MsgId" in msg else "system"
            self.fromUserName = msg["FromUserName"] if "FromUserName" in msg else None
            self.toUserName = msg["ToUserName"] if "ToUserName" in msg else None
            self.msgType = MessageType.of(msg["MsgType"]) if "MsgType" in msg else None
            self.content = msg["Content"] if "Content" in msg else None
            self.timestamp = msg["CreateTime"] if "CreateTime" in msg else None
            self.mediaId = msg["MediaId"] if "MediaId" in msg else None
            self.voiceLength = msg["VoiceLength"] if "VoiceLength" in msg else None
            self.fileName = msg["FileName"] if "FileName" in msg else None
            if (self.fromUserName[:2] == "@@") or (self.toUserName[:2] == "@@"):
                self.chatroom = True
            else:
                self.chatroom = False
            self.actualUserName = msg["ActualUserName"] if "ActualUserName" in msg else None
            self.actualNickName = msg["ActualNickName"] if "ActualNickName" in msg else None

    @property
    def pr(self):
        msg = self.__repr__()
        msg += (f"-||id:{self.id}, from:{self.fromUserName}, to:{self.toUserName}, timestamp:{time.ctime(self.timestamp)}, voiceLength:{self.voiceLength}, fileName:{self.fileName}"
                f"")
        return msg

    def __repr__(self):
        msg = ""
        if self.id == "system":
            return "System: " + self.content
        _a = ""
        if "<msg>" in self.content:
            _a = self.content
            self.content = "[卡片/转账等, 不予处理]"
        if (len(self.content) >= 20) and (self.content[1:].isalnum()):
            _a = self.content
            self.content = "[语音/图片等, 不予处理]"
        if self.toUserName == self.friends[0].md5:
            if self.chatroom:
                msg += f"Recv({Group.of(self.fromUserName).nickname}(群组)): [{self.msgType.name}]{self.content}"
            else:
                msg += f"Recv({Friend.of(self.fromUserName).nickname}/(朋友)): [{self.msgType.name}]{self.content}"
        elif self.fromUserName == self.friends[0].md5:
            if self.chatroom:
                msg += f"Send({Group.of(self.toUserName).nickname}(群组)): [{self.msgType.name}]{self.content}"
            else:
                msg += f"Send({Friend.of(self.toUserName).nickname}(好友)): [{self.msgType.name}]{self.content}"
        if "<msg>" in _a:
            self.content = _a
        if (len(_a) >= 1) and (_a[1:].isalnum()):
            self.content = _a
        return msg

    @classmethod
    def of(cls, msgId: str, messes: "list[Message]"):
        """
        从列表和id找到某一信息
        :param msgId:
        :param messes:
        :return:
        """
        for _m in messes:
            if _m.id == msgId:
                return _m
        return None

    def __str__(self):
        return self.__repr__()


class IChatBase:
    """
    抽象基类
        1.本类只实现基础方法
        2.监听策略, 监听后的函数可继承后重写
    """
    groups: list[Group] = list()  # 群组列表
    friends: list[Friend] = list()  # 好友列表
    login_path: str = "./login.ichat"  # 登录信息存储位置
    login_save: bool  # 是否保存登录信息
    thread: bool  # 是否线程监听
    msgs: list[Message] = []  # 消息队列
    out: bool = True  # 是否输出msg内容到控制台
    msg_types: list[MessageType] = list()  # 消息类型列表
    interceptors: dict[MessageType, list[MethodType]] = {_t: [] for _t in msg_types}  # 拦截器列表, 当有多个拦截对象时, 会顺序调用函数

    _listener: bool = False  # True为处理进程应该中断了

    def __init__(self, path: str = None, login_save: bool = True, thread: bool = True, out: bool = True):
        """
        IChat的抽象基础类
            1.监听消息
            2.自动判断类型
            3.自动回复
            4.保存登录状态
        :param path: 登录状态保存位置和读取位置
        :param login_save: 是否保存登录信息
        :param thread: 是否使用线程监听
        :param out: 是否输出每条msg的信息, 格式化msg
        """
        if path is not None:
            self.login_path = path
        self.login_save = login_save
        self.thread = thread
        self.out = out
        self.core = Core()

    def login(self, path: str = None):
        """
        登录微信
        :param path: 微信状态信息存储位置
        :return: none
        """
        if (path is not None) and os.path.exists(path):
            self.login_path = path
        if os.path.exists(self.login_path):
            self.core.load_login_status(self.login_path)
        self.core.login()
        if self.login_save:
            self.core.dump_login_status(self.login_path)
        self.friends = [Friend().loading(friend) for friend in self.core.get_friends()]
        self.groups = [Group().loading(group) for group in self.core.get_chatrooms()]
        self.core.get_friends(update=True)
        Message.friends = self.friends
        Message.groups = self.groups
        Message.messageTypes = self.msg_types
        Friend.friends = self.friends
        Group.groups = self.groups
        # print(self.friends)

    def listen(self, listen_exit: Callable = None):
        """
        监听函数, 启动消息监听和处理监听
        :param listen_exit: 程序退出函数, 设置后会阻塞进程
        :return: none
        """
        self.core.start_receiving(self.exit)  # 启动处理
        if self.thread:  # 线程启动
            threading.Thread(target=self._listening, daemon=True).start()
        else:  # 主线程携带
            self._listening()
        if listen_exit is not None:
            listen_exit()

    @staticmethod
    def listen_exit(ic_: "IChatBase"):
        """
        默认的退出函数
        :param ic_: 类实例
        :return: none
        """
        while True:
            try:
                time.sleep(0.05)
                if ic_._listener:
                    break
            except KeyboardInterrupt:
                break

    def _listening(self):
        """
        处理接受的消息
        :return: none
        """
        msgs: list[dict] = list()
        while True:
            if self._listener:
                break
            if not self.core.msgList.empty():
                _ms = self.core.msgList.get()
                if ("MsgId" in _ms) and (_ms["MsgId"] in msgs):
                    continue
                if "MsgId" not in _ms:
                    # 处理系统类型
                    continue
                msgs.append(_ms["MsgId"])
                ms_: Message = Message(_ms)
                self.msgs.append(ms_)
                print(_ms)
                if self.out:
                    # print(ms_)
                    pass
                # 以上的msgs为自处理消息内容, 以下的为系统自动处理的内容
                if ms_.id == "system":
                    self.system(_ms)
                else:
                    methods: list[MethodType] = self.interceptors.get(ms_.msgType, None)
                    if methods is None:
                        print(f"Error: 存在一种不常见的类型未装配拦截器({ms_.msgType.name})")
                    else:
                        for method in methods:
                            method(ms_, self)

    @abc.abstractmethod
    def system(self, msg: str):
        """
        处理类型为system的msg
        与其他类型分开处理
        :param msg: msg
        :return: none
        """

    def auto(self, types: list[MessageType]):
        """
        装饰器函数
        接受参数为消息类型, 注册到可执行的函数列表
        :param types: 接受的消息类型
        :return: none
        """

        def decorator(func: Callable[[Message, "IChatBase"], None]):
            for _t in types:
                if _t in self.interceptors:
                    self.interceptors[_t].append(func)
                else:
                    self.interceptors[_t] = [func]

            def wrapper(msg: Message, ic_: IChatBase):
                func(msg, ic_)

            return wrapper

        return decorator

    def exit(self):
        """
        退出函数, 当监听停止时调用的函数
        :return: none
        """
        self._listener = True
        return self._exit()

    @abc.abstractmethod
    def _exit(self):
        """
        用户自定义的退出策略
        :return: none
        """


mts: list[MessageType] = [
    MessageType(1, "文本"),  # 位置也是1
    MessageType(47, "表情"),
    MessageType(51, "定位"),
    MessageType(3, "图片"),
    MessageType(34, "语音"),
    MessageType(10000, "红包/拍一拍"),
    MessageType(49, "转账/文件/音乐/卡片"),  # 文件, 音乐
    MessageType(42, "名片"),
    
    MessageType(37, "未知"),
    MessageType(10002, "撤回")
]


class IChat(IChatBase):

    def system(self, msg: str):
        pass

    def _exit(self):
        return False


if __name__ == '__main__':
    # 初始化消息类型
    MessageType.cls_msssage_types = mts
    ic = IChat()
    ic.login()
    ic.listen()
    input()
