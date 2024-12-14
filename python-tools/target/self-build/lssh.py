import os
import json
from json import JSONDecodeError
import sys

path: str = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "data", "lsshd.json")
if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "data")):
    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "data"))
try:
    with open(path, "r") as f:
        data = json.load(f)
except (JSONDecodeError, FileNotFoundError):
    with open(path, "w") as f:
        json.dump([], f, indent=4)
        data = []


class Connect:

    def __init__(self):

        self.remark: str = None  # 连接的别名
        self.ip: str = None  # 连接的ip
        self.port: int = 22  # 连接的端口
        self.password: str = None  # 连接的的密码
        self.user: str = None  # 连接的用户

    def __repr__(self):
        return f"{self.ip}:{str(self.port)}-> {self.remark}"

    @classmethod
    def of(cls, remark: str, _cs: "list[Connect]"):
        """
        通过remark获取连接
        :param remark: 别名
        :param _cs: 连接列表
        :return: connect
        """
        for _cc in _cs:
            if _cc.remark == remark:
                return _cc

    @classmethod
    def save(cls, _cs: "list[Connect]"):
        __: list = list()
        for _cc in _cs:
            _: dict = {
                "remark": _cc.remark,
                "ip": _cc.ip,
                "port": _cc.port,
                "user": _cc.user,
                "password": _cc.password,
            }
            __.append(_)
        with open(path, "w") as _f:
            json.dump(__, _f, indent=4)


cons: list[Connect] = list()
for con in data:
    _c = Connect()
    _c.ip = con["ip"]
    _c.port = con["port"]
    _c.password = con["password"]
    _c.remark = con["remark"]
    _c.user = con["user"]
    cons.append(_c)

import sys
if len(sys.argv) == 1:
    try:
        sys.argv.append(cons[0].remark)
    except IndexError:
        sys.argv.append("path")

if sys.argv[1] == "list":
    for con in cons:
        print(con)

elif sys.argv[1] == "add":
    try:
        c = Connect()
        c.remark = input("remark: ")
        c.ip = input("ip: ")
        c.port = input("port: ")
        if c.port:
            c.port = int(c.port)
        else:
            c.port = 22
        c.password = input("password: ")
        c.user = input("user: ")
        cons.append(c)
        Connect.save(cons)
    except Exception as e:
        print("添加失败:", e)
elif sys.argv[1] == "remove":
    if len(sys.argv) == 3:
        remark = sys.argv[2]
    else:
        remark = input("remark: ")
    for con in cons:
        if con.remark == remark:
            cons.remove(con)
            Connect.save(cons)
            break
    else:
        print(f"remark not found ({remark})")
elif sys.argv[1] == "path":
    print(path)
else:
    for con in cons:
        if con.remark == sys.argv[1]:
            command: str = rf"plink -l {con.user} -pw {con.password} -P {con.port} -batch {con.ip}"
            print(command)
            os.system(command)
            break
        else:
            print("none")