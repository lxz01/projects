# 定义需要的基本类型


# 基本消息类型处理
from typing import Any


class ContentType:
    """
    基本类型
    """
    id: int = -1  # 编号
    sub: int = -1  # 子编号
    name: str = "Null"  # 名称
    remark: str = "Null"  # 替代名称

    ContentTypes: list['ContentType'] = []  # 所有类型, 需要后手输入

    def __init__(self, id: int, sub: int, name: str, remark: str):
        self.id = id
        self.sub = sub
        self.name = name
        self.remark = remark
    
    @classmethod
    def of(self, id: int, sub: int):
        """
        通过id和sub获取类型
        """
        for i in self.ContentTypes:
            if i.id == id and i.sub == sub:
                return i
        print(id, sub)
        return ContentType(-1, -1, "Null", "Null")

    @classmethod
    def find(self, remark: str):
        """
        通过替代名称获取类型
        """
        for i in self.ContentTypes:
            if i.remark == remark:
                return i
        return ContentType(-1, -1, "Null", "Null")

cons: list[ContentType] = [
    ContentType(1, 0, "文本", "text"),
    ContentType(3, 0, "图片", "picture"),
    ContentType(34, 0, "语音", "voice"),
    ContentType(42, 0, "名片", "card"),
    ContentType(43, 0, "视频", "video"),
    ContentType(47, 0, "动画表情", "emoji"),
    ContentType(49, 1, "链接文本", "linktext"),
    ContentType(49, 5, "链接卡片", "linkcard"),
    ContentType(49, 6, "文件", "file"),
    ContentType(49, 8, "gif表情", "gif"),
    ContentType(49, 19, "聊天记录", "chatrecord"),
    ContentType(49, 33, "分享程序", "shareapp"),
    ContentType(49, 36, "分享程序", "shareapp2"),
    ContentType(49, 57, "引用文本", "quotetext"),
    ContentType(49, 63, "视频/直播", "video2"),
    ContentType(49, 87, "群公告", "announcement"),
    ContentType(49, 88, "视频/直播", "video3"),
    ContentType(49, 2000, "转账消息", "transfer"),
    ContentType(49, 2003, "红包封面", "redpacket"),
    ContentType(51, 0, "其他终端定位到此聊天", "transfer"),
    ContentType(10000, 0, "系统通知", "system"),
    ContentType(10000, 4, "拍一拍", "pokes"),
    ContentType(10000, 8000, "邀请聊天", "invite"),
    ContentType(10002, 0, "撤回", "invite"),
    ]
ContentType.ContentTypes = cons  # 方便进行查找


class Member:
    """
    Friend和Group的继承基类
    """
    md5: str = None  # 成员的md5

    members: list["Member"] = list()  # 群组和用户公共查询

    @classmethod
    def of(cls, md5: str):
        """
        通过md5获取成员
        """
        for i in cls.members:
            if i.md5 == md5:
                return i
        return Member()

    @classmethod
    def find(cls, remark: str):
        """
        通过备注获取成员
        """
        for i in cls.members:
            if i.remark == remark:
                return i
        return Member()

    @classmethod
    def expend(cls, lis: list["Member"]):
        """
        批量添加成员
        """
        cls.members.extend(lis)
    
    def __getattribute__(self, name: str) -> Any:
        """
        当调用不存在的属性时, 自动调用fromUser的属性
        """
        if name not in object.__getattribute__(self, "__dict__"):
            return "Null"
        return super().__getattribute__(name)


# 基本消息对象处理(成员, 群组)
class Friend(Member):
    md5: str = None  # 微信号哈希
    nickname: str = None  # 昵称
    headimg: str = None  # 头像地址
    remark: str = None  # 备注
    sex: str = None  # 性别
    signature: str = None  # 个性标签
    province: str = "None"  # 省份
    city: str = "None"  # 城市
    star: bool = None  # 星标
    room: "Group" = None  # 所属群组, 为None则是好友
    friends: list["Friend"] = list()  # 优先接受类属性friends
    temps: list["Friend"] = list()  # 接受群组临时成员信息

    def __init__(self, msg: dict):
        """
        通过msg加载信息
        :param msg: 消息
        :return: self
        """
        self.md5 = msg["UserName"] if "UserName" in msg else None
        self.nickname = msg["NickName"] if "NickName" in msg else None
        self.headimg = msg["HeadImgUrl"] if "HeadImgUrl" in msg else None
        self.remark = msg["RemarkName"] if "RemarkName" in msg else None
        self.signature = msg["Signature"] if "Signature" in msg else None
        self.star = msg["StarFriend"] if "StarFriend" in msg else False
        self.province = msg["Province"] if "Province" in msg else None
        self.city = msg["City"] if "City" in msg else None
        if "Sex" not in msg:
            self.sex = "未知"
        else:
            if msg["Sex"] == 1:
                self.sex = "男"
            elif msg["Sex"] == 0:
                self.sex = "女"
            else:
                self.sex = "未知"
    
    @classmethod
    def of(self, md5: str = None):
        """
        通过md5获取好友
        """
        if md5 == None:
            return self.friends[0]
        for i in self.friends:
            if i.md5 == md5:
                return i
        for i in self.temps:
            if i.md5 == md5:
                return i
        return Friend({})
    
    @classmethod
    def find(cls, remark: str = None):
        """
        通过备注获取好友
        """
        if remark == None:
            return cls.friends[0]
        for i in cls.friends:
            if i.remark == remark:
                return i
        for i in cls.temps:
            if i.remark == remark:
                return i
        return Friend({})

    @classmethod
    def expend(cls, lis: list["Friend"], temp: bool = False):
        """
        添加群组临时或好友
        """
        if temp:
            cls.temps.extend(lis)
        else:
            cls.friends.extend(lis)
        cls.members.extend(lis)


class Group(Member):
    md5: str = None  # 群号
    nickname: str = None  # 群昵称

    groups: list["Group"] = list()  # 优先接受类属性groups
    
    def __init__(self, msg: dict):
        """
        通过msg加载信息
        :param msg: 消息
        :return: self
        """
        self.md5 = msg["UserName"] if "UserName" in msg else None
        self.nickname = msg["NickName"] if "NickName" in msg else None

    @classmethod
    def of(cls, md5: str):
        """
        通过md5获取群组
        """
        for i in cls.members:
            if i.md5 == md5:
                return i
        return Group({})

    def __getattribute__(self, name: str) -> Any:
        """
        当调用不存在的属性时, 自动调用fromUser的属性
        """
        if name not in object.__getattribute__(self, "__dict__"):
            return "Null"
        return super().__getattribute__(name)

    @classmethod
    def find(cls, remark: str):
        """
        通过备注获取群组
        """
        for i in cls.members:
            if i.remark == remark:
                return i
        return Group({})
    @classmethod
    def expend(cls, lis: list["Group"]):
        """
        添加群组
        """
        cls.groups.extend(lis)
        cls.members.extend(lis)


# 基础消息定义
class Message:
    id: str  # 消息的id
    fromUser: Member  # 消息来源用户
    toUser: Member  # 消息目标用户
    msgType: ContentType  # 消息类型
    content: str  # 消息
    timestamp: int  # 消息时间戳
    voiceLength: int  # 语音时长, 毫秒
    fileName: str  # 当为文件或图片时
    mediaId: str  # 文件下载路径

    # 群聊专有msg信息
    chatroom: bool  # 是否为群聊
    actualUserName: str  # 当前发消息的用户id
    actualNickName: str  # 当前发消息的用户昵称
    actual: Member  # 当前说话的成员

    messages: list["Message"] = list()  # 消息列表, 用于查找消息

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
            self.fromUser = Member.of(msg["FromUserName"]) if "FromUserName" in msg else None
            self.toUser = Member.of(msg["ToUserName"]) if "ToUserName" in msg else None
            self.msgType = ContentType.of(msg["MsgType"], msg["AppMsgType"]) if "MsgType" in msg else None
            self.content = msg["Content"] if "Content" in msg else None
            self.timestamp = msg["CreateTime"] if "CreateTime" in msg else None
            self.mediaId = msg["MediaId"] if "MediaId" in msg else None
            self.voiceLength = msg["VoiceLength"] if "VoiceLength" in msg else None
            self.fileName = msg["FileName"] if "FileName" in msg else None
            if isinstance(self.fromUser, Group):
                self.chatroom = True
            elif isinstance(self.toUser, Group):
                self.chatroom = True
            else:
                self.chatroom = False
            self.actualUserName = msg["ActualUserName"] if "ActualUserName" in msg else None
            self.actualNickName = msg["ActualNickName"] if "ActualNickName" in msg else None
            for _ in msg["User"]["MemberList"]:
                self._group_add_temp(_)
            self.actual = Member.of(self.actualUserName) if self.actualUserName else None
    
    def __repr__(self) -> str:
        """
        输出消息
        """
        if self.chatroom:
            know: str = ""
            rem = Friend.of(self.actual.md5)
            if rem.remark is not None:
                if rem.md5 == Friend.friends[0].md5:
                    know = f"(大帅哥)"
                else:
                    know = f"(好友)"
            return F"{self.fromUser.remark}({self.fromUser.nickname})->{self.toUser.remark}({self.toUser.nickname})|{self.actual.remark}({self.actual.nickname}[{know}]): [{self.msgType.name}] {self.content}"
        return F"{self.fromUser.remark}({self.fromUser.nickname})->{self.toUser.remark}({self.toUser.nickname}): [{self.msgType.name}]{self.content}"
    
    def _group_add_temp(self, _d: dict):
        """
        通过msg获取到的成员, 添加到临时成员列表
        """
        _f = Friend(_d)
        _f.room = self.fromUser if isinstance(self.fromUser, Group) else self.toUser
        Friend.expend([_f], temp=True)
    
    @classmethod
    def add(cls, msg: "Message"):
        """
        添加消息
        """
        if msg.id in [i.id for i in cls.messages]:
            return False
        cls.messages.append(msg)
        return True

    @classmethod
    def find(cls, id: str):
        """
        通过id查找消息
        """
        for i in cls.messages:
            if i.id == id:
                return i
        return Message({})
    

class IChat:
    """
    启动微信
    """
    import os
    from source.ichat.itchat import Core
    import threading
    _login_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "login.ichat")  # 登录信息存储位置
    _listener: bool = False  # 监听状态

    def __init__(self, is_send: bool = True) -> None:
        """
        登录微信
        :param is_send: 是否可以发送信息
        """
        self.core = self.Core()
        if self.os.path.exists(self._login_path):
            print(self._login_path)
            self.core.load_login_status(self._login_path)
        self.core.login()
        self.core.load_login_status(self._login_path)
        self.core.dump_login_status(self._login_path)
        Friend.expend([Friend(friend) for friend in self.core.get_friends()])
        Group.expend([Group(group) for group in self.core.get_chatrooms()])
        Friend.friends[0].nickname = "大帅哥"
        Friend.friends[0].remark = "大帅哥"
        self.core.start_receiving(self.exit)
        if is_send:
            self.threading.Thread(target=self._listen).start()
            self._send()
        else:
            self._listen()
    
    def _send(self):
        """
        发送信息
        """
        return self.send()

    def send(self):
        """
        自定义的send函数
        """
        return input()

    def _listen(self):
        """
        监听消息
        """
        while True:
            if self._listener:
                break
            if self.core.msgList.empty():
                continue
            msg = self.core.msgList.get()
            message = Message(msg)
            if Message.add(message):
                # 可处理的消息
                print(msg["Text"])
                self._deal(message)
    
    def _deal(self, msg: Message):
        """
        处理消息
        """
        print(msg)

    def exit(self):
        """
        退出函数, 当监听停止时调用的函数
        :return: none
        """
        self._listener = True
        return self._exit()

    def _exit(self):
        """
        退出函数, 当监听停止时调用的函数
        :return: none
        """
        return None


if __name__ == "__main__":
    IChat()
from source.ichat import itchat
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg['Text']