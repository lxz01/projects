from cryptography.fernet import Fernet
import hashlib
import os
import base64
import uuid
from typing import Callable
import json


class FernetException(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


class EncFile:
    """
    加密文件的存储信息
    """
    name: str = None
    data: bytes = None
    path: str = None
    
    def __init__(self, path: str | None = None) -> None:
        if path is None:
            return
        self.path = path
        if not os.path.isfile(path):
            raise FernetException(f"文件不存在{path}")
        with open(path, "rb") as f:
            self.data = f.read()
        self.name = os.path.basename(self.path)
    
    def __setstate__(self, state) -> object:
        self.__dict__.update(state)
    
    def to_json(self) -> dict:
        state =  {
            "name": self.name,
            "data": base64.b64encode(self.data).decode("utf-8"),
            "path": self.path
        }
        return state
    
    def from_json(self, state: dict) -> None:
        self.__dict__.update(state)
        self.data = base64.b64decode(self.data)
    
    def __getstate__(self) -> object:
        return {
            "name": self.name,
            "data": base64.b64decode(self.data),
            "path": self.path
        }


class EncFolder:
    """
    加密文件夹的存储信息
    """
    name: str = None
    path: str = None
    files: list[EncFile] = []
    folders: "list[EncFolder]" = []
    
    def __init__(self, path: str | None = None) -> None:
        if path is None:
            return
        self.path = path
        self.name = os.path.basename(self.path)
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)):
                self.files.append(EncFile(os.path.join(path, i)))
            elif os.path.isdir(os.path.join(path, i)):
                self.folders.append(EncFolder(os.path.join(path, i)))
    
    
    def load(self) -> None:
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        for i in self.files:
            i.path = os.path.join(self.path, i.name)
            with open(i.path, "wb") as f:
                f.write(i.data)
        for i in self.folders:
            i.path = os.path.join(self.path, i.name)
            if not os.path.isdir(i.path):
                os.mkdir(i.path)
            i.load()
    
    def __setstate__(self, state) -> None:
        self.__dict__.update(state)
        for i in state["files"]:
            _i = EncFile()
            _i.__dict__.update(i)
            self.files.append(_i)

    def __getstate__(self) -> object:
        state = self.__dict__.copy()
        state["files"] = [i.__getstate__() for i in self.files]
        state["folders"] = [i.__dict__ for i in self.folders]
        return state
    
    def to_json(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "files": [i.to_json() for i in self.files],
            "folders": [i.to_json() for i in self.folders if not len(i.folders)]
        }
    
    def from_json(self, state: dict) -> None:
        self.name = state["name"]
        self.path = state["path"]
        for i in state["files"]:
            _i = EncFile()
            _i.from_json(i)
            self.files.append(_i)
        for i in state["folders"]:
            _i = EncFolder()
            _i.from_json(i)
            self.folders.append(_i)


class _Encoder:

    def __init__(self, _fr: Fernet) -> None:
        self._key: Fernet = _fr
    
    def string(self, data: str) -> str:
        return self._key.encrypt(data.encode("utf-8")).decode("utf-8")

    def byte(self, data: bytes) -> bytes:
        return self._key.encrypt(data)

    def file(self, _f: EncFile | str) -> EncFile:
        if isinstance(_f, str):
            _f = EncFile(_f)
        if ".lefer" in _f.name:
            raise FernetException(f"不得二次加密文件{_f.name}")
        if ".leder" in _f.name:
            raise FernetException(f"不支持文件夹再加密{_f.name}")
        _p = os.path.join(os.path.dirname(_f.path), f"{str(uuid.uuid4())}.lefer")
        with open(_p, "wb") as f:
            f.write(self._key.encrypt(json.dumps(_f.to_json()).encode("utf-8")))
        _e = EncFile(_p)
        os.remove(_f.path)
        return _e

    def dir(self, _f: EncFolder | str) -> EncFile:
        if isinstance(_f, str):
            _f = EncFolder(_f)
        if ".lefer" in _f.name:
            raise FernetException(f"不得二次加密文件夹{_f.name}")
        if ".leder" in _f.name:
            raise FernetException(f"不支持文件夹再加密{_f.name}")
        _p = os.path.join(os.path.dirname(_f.path), f"{str(uuid.uuid4())}.leder")
        with open(_p, "wb") as f:
            _e = self._key.encrypt(json.dumps(_f.to_json()).encode("utf-8"))
            f.write(_e)
        _e = EncFile(_p)
        return _e


class _Decoder:

    def __init__(self, _fr: Fernet) -> None:
        self._key: Fernet = _fr
    
    def string(self, data: str) -> str:
        return self._key.decrypt(data.encode("utf-8")).decode("utf-8")
    
    def byte(self, data: bytes) -> bytes:
        return self._key.decrypt(data)
    
    def file(self, _f: EncFile | str) -> EncFile:
        if isinstance(_f, str):
            _f = EncFile(_f)
        if ".lefer" not in _f.name:
            raise FernetException(f"文件名错误{_f.name}")
        obj = EncFile()
        obj.from_json(eval(self._key.decrypt(_f.data).decode("utf-8")))
        _p = os.path.join(os.path.dirname(_f.path), f"{obj.name}")
        with open(_p, "wb") as f:
            f.write(obj.data)
        obj.path = _p
        os.remove(_f.path)
        return obj
    
    def dir(self, _f: EncFile | str) -> EncFolder:
        if isinstance(_f, str):
            _f = EncFile(_f)
        if ".lefer" in _f.name:
            raise FernetException(f"此方法不能解密文件夹{_f.name}")
        obj = EncFolder()
        obj.from_json(eval(self._key.decrypt(_f.data).decode("utf-8")))
        _p = os.path.join(os.path.dirname(_f.path), f"{obj.name}")
        obj.path = _p
        obj.load()
        return obj

class Encipher:
    """
    字符串/字节流/文件/文件夹加密
    """
    password: str = None  # 加密的密码
    key: Fernet = b""  # 加密的密钥
    data: bytes = b""  # 被加密的文件

    @classmethod
    def _md5(cls, data: str) -> bytes:
        md5_hash = hashlib.md5(data.encode("utf-8")).digest()
        # 使用PBKDF2算法生成32字节的密钥
        key = hashlib.pbkdf2_hmac('sha256', md5_hash, b'salt_', 100000)
        # 将密钥转换为url-safe base64编码的字节
        return base64.urlsafe_b64encode(key)

    def __init__(self, password: str):
        self.password = password
        _key = self._md5(password)
        self.key = Fernet(_key)
        self.decoder = _Decoder(self.key)
        self.encoder = _Encoder(self.key)
    

import sys
enc = Encipher("041216")
if len(sys.argv) == 3:
    if sys.argv[1] == "decode":
        if os.path.splitext(sys.argv[2])[-1] == ".leder":
            enc.decoder.dir(sys.argv[2])
        elif os.path.splitext(sys.argv[2])[-1] == ".lefer":
            enc.decoder.file(sys.argv[2])
        else:
            print(f"文件不正确({sys.argv[2]})")
    elif sys.argv[1] == "encode":
        if os.path.isdir(sys.argv[2]):
            enc.encoder.dir(sys.argv[2])
        elif (os.path.isfile(sys.argv[2])) and (os.path.splitext(sys.argv[2])[-1] not in (".lefer", ".leder")):
            enc.encoder.file(sys.argv[2])
        else:
            print("文件不正确")
    else:
        print("参数不正确")
else:
    print("参数不正确")
