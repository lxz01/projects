import os
import sys
path: str = "./help"
print(os.getcwd())


if len(sys.argv) == 1:
    for _p in os.listdir(path):
        if ".txt" not in _p:
            continue
        print(f"File: {_p}")
        with open(os.path.join(path, _p), "r", encoding="utf-8") as f:
            print(f.read())
        print()

elif len(sys.argv) == 2:
    sys.argv[1] = sys.argv[1] + ".txt"
    print(f"File: {sys.argv[1]}")
    if os.path.exists(os.path.join(path, sys.argv[1])):
        with open(os.path.join(path, sys.argv[1]), "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Help: 文件不存在, 请检查文件名")
    print()

else:
    print("Help: 文件不存在, 请检查文件名")