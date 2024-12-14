from source import mts, Message, MessageType, Friend, Group
from source import IChat

iChat = IChat("./login.ichat")
iChat.login()
MessageType.cls_msssage_types = mts

@iChat.auto(mts[:-1])
def output(msg: Message, iChat: IChat):
    # if not msg.chatroom:
    #     print(msg.__repr__())
    # else:
    #     if msg.toUserName == iChat.friends[0].md5:
    #         print(msg.__repr__())
    #     else:
    #         print(msg.__repr__())
    pass

@iChat.auto(mts[-1:])
def withdraw(msg: Message, iChat: IChat):
    # ms: str = "[未知信息]"  # 撤回的信息
    # s = msg.content.split("<msgid>")[1].split("<")[0]
    # for _m in iChat.msgs:
    #     if _m.id == s:
    #         ms = f"({_m.__repr__()})"
    # if not msg.chatroom:
    #     if msg.toUserName == iChat.friends[0].md5:
    #         print(f"你的朋友-> {Friend.of(_id=msg.fromUserName).nickname}: [撤回了]{ms}")
    #     else:
    #         print(f"你({iChat.friends[0].nickname})-> {Friend.of(_id=msg.toUserName).nickname}: [撤回了]{ms}")
    # else:
    #     if msg.fromUserName == iChat.friends[0].md5:
    #         print(f"你({iChat.friends[0].nickname})-> {Group.of(_id=msg.toUserName).nickname}: [撤回了]{ms}")
    #     else:
    #         print(f"{Group.of(_id=msg.fromUserName).nickname}: [撤回了]{ms}")
    pass


# iLoading = IChatLoading(iChat, "./chat.txt")
iChat.listen()
input()
