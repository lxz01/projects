from source.ichat import itchat
from source.ichat.itchat.content import TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO, FRIENDS, SYSTEM
import time, os

chating: list[dict] = list()
fpath: str = fr"./python-tools/data/wechat_files"

if not os.path.exists(fpath):
   os.makedirs(fpath)
if not os.path.exists(fpath+"/data"):
   os.makedirs(fpath+"/data")
print(f'Wechat path: {os.path.join(fpath, "wechat.txt")}')

# 下载文件到本地
def download_files(msg):
   msg.download(fpath+"/data/"+msg['FileName'])
   return fpath+"/data/"+msg['FileName']


def chatroom(md: str):
   for i in itchat.get_chatrooms():
      if i["UserName"] == md:
         return i
   return {
      "UserName": md,
      "NickName": "[未知]",
      "MemberCount": 0,
   }

def friend(md: str):
   for i in itchat.get_friends():
      if i == itchat.get_friends()[0]:
         i["RemarkName"] = "我"
      if i["UserName"] == md:
         i["RemarkName"] = i["RemarkName"] if "RemarkName" in i else "Null"
         return i
   return {
      "UserName": md,
      "RemarkName": "[未知]",
      "NickName": "[未知]",
      "MemberCount": 0,
   }

def filehelper(msg: dict):
   """
   防撤回, 发送到文件传输助手
   """
   _m = ""
   if "@@" in msg["FromUserName"]:
      _m += "[撤回]来自群聊" + chatroom(msg["FromUserName"])["NickName"] + f"({msg['ActualNickName']}): " + msg["Content"]
   elif "@@" in msg["ToUserName"]:
      return
   elif (msg["FromUserName"] == itchat.get_friends()[0]["UserName"]) or (msg["ToUserName"] == "filehelper"):
      return
   else:
      _m += "[撤回]来自好友" + friend(msg["FromUserName"])["NickName"] + f"({friend(msg['FromUserName'])['RemarkName']}): " +  msg["Content"]
   if (len(msg["Content"]) > 3) and (msg["Content"][:4] == "[撤回]"):
      if (len(msg["Content"]) > 7) and msg["Content"][4:8] in ("[图片]", "[语音]", "[文件]", "[视频]"):
         path = msg["Content"][8:]
         itchat.send_msg(_m, toUserName="filehelper")
         itchat.send_file(path, toUserName="filehelper")
         return
   itchat.send_msg(_m, toUserName="filehelper")
   return


def output(msg: dict):
   _m = ""
   if "@@" in msg["FromUserName"]:
      _m += chatroom(msg["FromUserName"])["NickName"] + f"({msg['ActualNickName']}): " + msg["Content"]
   elif "@@" in msg["ToUserName"]:
      _m += chatroom(msg["ToUserName"])["NickName"] + f"({msg['ActualNickName']}): " + msg["Content"]
   else:
      _m += friend(msg["FromUserName"])["NickName"] + F'({friend(msg["FromUserName"])["RemarkName"]})' + f'-> {friend(msg["ToUserName"])["NickName"]}({friend(msg["ToUserName"])["RemarkName"]}): ' + msg["Content"]
   print("> " + _m)
   chating.append(msg)
   if ("CreateTime" not in msg):
      print(1)
      return
   if ("FromUserName" not in msg):
      print(2)
      return
   if ("ToUserName" not in msg):
      print(3)
      return
   with open(os.path.join(fpath, "wechat.txt"), "a+", encoding="utf-8") as f:
      f.write(
         _m + f'\t({time.ctime(msg["CreateTime"])})[{msg["FromUserName"]}-> {msg["ToUserName"]}]' + "\n"
      )
   

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING,PICTURE,RECORDING,ATTACHMENT,VIDEO,FRIENDS,SYSTEM], True, True)
def reply_mseeage(msg):
   if (msg["FromUserName"] == "filehelper") or (msg["ToUserName"] == "filehelper"):
      return None
   if msg['Type'] == TEXT:
      output(msg)
   if msg['Type'] == MAP:
      msg["Content"] = msg["Content"].split("\n")[0]
      output(msg)
   if msg['Type'] == CARD:
      msg["Content"] = "[Card]" + msg["Content"]
      output(msg)
   if msg['Type'] == NOTE:
      if "<msgid>" in msg["Content"]:
         _id = msg["Content"].split("<msgid>")[1].split("</msgid>")[0]
         for i in chating:
            if "MsgId" not in i:
               continue
            if i["MsgId"] == _id:
               msg["Content"] = "[撤回]" + i["Content"]
               output(msg)
               filehelper(msg)
               return None
      msg["Content"] = "[Note]" + msg["Content"]
      output(msg)
   if msg['Type'] == SHARING:
      msg["Content"] = "[Sharing]" + msg["Content"]
      output(msg)
   if msg['Type'] == PICTURE:
      msg["Content"] = "[图片]" + download_files(msg)
      output(msg)
   if msg['Type'] == RECORDING:
      msg["Content"] = "[语音]" + download_files(msg)
      output(msg)
   if msg['Type'] == ATTACHMENT:
      msg["Content"] = "[文件]" + download_files(msg)
      output(msg)
   if msg['Type'] == VIDEO:
      msg["Content"] = "[视频]" + download_files(msg)
      output(msg)
   if msg['Type'] == FRIENDS:
      msg["Content"] = "[好友请求]" + msg["Content"]
      output(msg)
   if msg['Type'] == SYSTEM:
      try:
         msg["Content"] = "[系统通知]" + msg["Content"]
      except KeyError:
         msg["Content"] = "[系统通知]"
      output(msg)
   return None;
itchat.auto_login(hotReload=True)
itchat.run()
