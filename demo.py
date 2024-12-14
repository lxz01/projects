from basic import rpc
from basic import Window

Window.list().foreach(Window.Print.print_exclude_no_title)
rpc.RpcServer()
