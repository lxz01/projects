# from basic import rpc
from basic import Window

Window.list().foreach(Window.Print.print_exclude_no_title)
Window.list().foreach(lambda hwnd, index: Window(hwnd).minimize())
# rpc.RpcServer()
