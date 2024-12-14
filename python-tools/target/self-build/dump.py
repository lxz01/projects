"""
文件导出
"""
import os
import sys


def dump(src: str, dst: str, ignore: bool = False):
    """
    复制文件到另一个文件夹
    :param src: 源文件
    :param dst: 目标文件
    :param ignore: 是否忽略文件存在
    :return: none
    """
    if not os.path.exists(src):
        print("源文件不存在")
        return
    if os.path.exists(dst):
        print("目标文件已存在")
        return
    with open(src, "rb") as f:
        with open(dst, "wb") as g:
            g.write(f.read())


if len(sys.argv) >= 3:
    if sys.argv[3] == "-i" or sys.argv[3] == "--ignore":
        dump(sys.argv[1], sys.argv[2], True)
    dump(sys.argv[1], sys.argv[2])
else:
    print("Usage: python dump.py <src> <dst>")
