"""
窗口控制
"""
import win32gui, win32con # type: ignore
from enum import Enum
from basic.utils import ListPlus
from basic.error import LxzBaseExpection


class WindowException(LxzBaseExpection):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class _WindowActive(Enum):
    """
    窗口活跃状态
    """
    active = 1  # 窗口活跃
    inactive = 0  # 窗口不活跃


class _WindowShowed(Enum):
    """
    窗口显示状态
    """
    showed = 1  # 窗口显示
    minimized = 2  # 窗口最小化
    maximized = 3  # 窗口最大化


class _WindowHidden(Enum):
    """
    窗口是否隐藏
    """
    normal = 1  #  正常显示
    hidden = 2  #  隐藏


class Window:
    """
    控制窗口
    """
    _handle: int = -1  #  窗口句柄
    _title: str = ""  # 窗口标题
    _class_name: str = ""  # 窗口类名
    _actived: _WindowActive = None  # 窗口活跃状态
    _showed: _WindowShowed = None  # 窗口显示状态
    _hidden: _WindowHidden = None  # 窗口是否隐藏
    _place: tuple = (0, 0)  # 窗口起始坐标
    _size: tuple = (0, 0)  # 窗口大小

    class Print:
        """
        输出类
        """
        @classmethod
        def print_exclude_no_title(cls, window: "Window", index: int = None) -> None:
            if window.title == "":
                return
            if index is not None:
                print(f"{index}< ", window)
                return
            print(window)
        
        @classmethod
        def print(cls, window: "Window", index: int = None) -> None:
            if index is not None:
                print(f"{index}< ", window)
                return
            print(window)
    
    Showed = _WindowShowed
    Active = _WindowActive
    Hidden = _WindowHidden


    def __init__(self, hwnd: int) -> None:
        self._handle = hwnd
        self._title = self.title
        self._class_name = self.class_name
        self._place = self.place
        self._size = self.size
        self._hidden = self.hidden
        self._actived = self.actived
        self._showed = self.showed
    
    def __repr__(self) -> str:
        return f"{self.handle}: {self.title}({self.class_name})| {self.place}{self.size}"
    

    @classmethod
    def list(cls) -> ListPlus['Window']:
        """
        获取所有窗口
        """
        def callback(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                ctx.append(Window(hwnd))
        windows: ListPlus["Window"] = ListPlus()
        win32gui.EnumWindows(callback, windows)
        return windows
    
    @classmethod
    def find(cls, /, _handle: int = None, _title: str = None, _class: str = None) -> "Window":
        """
        根据句柄、标题、类名查找窗口
        """
        if _handle is not None:
            return cls(_handle)
        if not ((_title is None) and (_class is None)):
            return cls(win32gui.FindWindow(_class, _title))
    
    @property
    def handle(self):
        """
        获取窗口句柄
        """
        return self._handle

    @property
    def title(self):
        """
        获取窗口标题
        """
        if not win32gui.IsWindow(self.handle):
            raise WindowException("无效的窗口句柄")
        if self._handle != -1:
            self._title = win32gui.GetWindowText(self._handle)
        return self._title

    @property
    def class_name(self):
        """
        获取窗口类名
        """
        if not win32gui.IsWindow(self.handle):
            raise WindowException("无效的窗口句柄")
        if self._handle != -1:
            self._class_name = win32gui.GetClassName(self._handle)
        return self._class_name

    @property
    def actived(self):
        """
        获取窗口活跃状态
        """
        if not win32gui.IsWindow(self.handle):
            raise WindowException("无效的窗口句柄")
        if win32gui.IsWindowEnabled(self.handle):
            return self.Active.active
        else:
            return self.Active.inactive

    @property
    def showed(self):
        """
        获取窗口显示状态
        """
        if not win32gui.IsWindow(self.handle):
            raise WindowException("无效的窗口句柄")
        placement = win32gui.GetWindowPlacement(self.handle)
        if placement[1] == win32con.SW_SHOWNORMAL:
            self._showed = self.Showed.showed
            return self.Showed.showed
        elif placement[1] == win32con.SW_SHOWMINIMIZED:
            self._showed = self.Showed.minimized
            return self.Showed.minimized
        elif placement[1] == win32con.SW_SHOWMAXIMIZED:
            return self.Showed.maximized
        else:
            raise WindowException(f"未知窗口状态({placement})")

    @property
    def place(self):
        """
        获取窗口起始坐标
        """
        if not win32gui.IsWindow(self.handle):
            raise WindowException("无效的窗口句柄")
        if self._handle != -1:
            self._place = win32gui.GetWindowRect(self._handle)[:2]
            if (self._place[0] >= 0) and (self._place[1] >= 0):
                pass
            else:
                self._place = (0, 0)
        return self._place


    @property
    def size(self):
        """
        获取窗口结束坐标
        """
        if not win32gui.IsWindow(self.handle):
            raise WindowException("无效的窗口句柄")
        if self._handle != -1:
            self._place = win32gui.GetWindowRect(self._handle)[:2]
            if (self._place[0] >= 0) and (self._place[1] >= 0):
                pass
            else:
                self._place = (0, 0)
            _end_coordinate = win32gui.GetWindowRect(self._handle)[2:]
            if (_end_coordinate[0] >= 0) and (_end_coordinate[1] >= 0):
                pass
            else:
                _end_coordinate = (0, 0)
            width = _end_coordinate[0] - self._place[0]
            height = _end_coordinate[1] - self._place[1]
            self._size = (width, height)
        return self._size

    @property
    def hidden(self):
        """
        获取窗口是否隐藏
        """
        if not win32gui.IsWindow(self.handle):
            raise WindowException("无效的窗口句柄")
        if win32gui.IsWindowVisible:
            self._hidden = self.Hidden.hidden
            return self.Hidden.hidden
        else:
            self._hidden = self.Hidden.hidden
            return self.Hidden.hidden
    
    @hidden.setter
    def hidden(self, value: bool):
        """
        设置窗口是否隐藏
        """
        if value:
            win32gui.ShowWindow(self._handle, win32con.SW_HIDE)
            self._hidden = self.Hidden.hidden
        else:
            win32gui.ShowWindow(self._handle, win32con.SW_SHOW)
            self._hidden = self.Hidden.showed
    
    @size.setter
    def size(self, value: tuple):
        """
        设置窗口大小
        """
        self._size = value
        win32gui.SetWindowPos(self._handle, 0, self._place[0], self._place[1], self._size[0], self._size[1], 0)

    @place.setter
    def place(self, value: tuple):
        """
        设置窗口起始坐标
        """
        self._place = value
        win32gui.SetWindowPos(self._handle, 0, self._place[0], self._place[1], self.size[0], self.size[1], 0)

    @handle.setter
    def handle(self, value: int):
        """
        设置窗口句柄
        """
        raise WindowException("不支持修改窗口句柄")

    @title.setter
    def title(self, value: str):
        """
        设置窗口标题
        """
        win32gui.SetWindowText(self._handle, value)
        self._title = value
    
    @actived.setter
    def actived(self, value: bool):
        """
        设置窗口活跃状态
        """
        if value:
            win32gui.SetForegroundWindow(self._handle)
            self._actived = self.actived
        else:
            win32gui.SetForegroundWindow(0)
            self._actived = self.actived
    
    @hidden.setter
    def hidden(self, value: bool):
        """
        设置窗口显示状态
        """
        if value:
            win32gui.ShowWindow(self._handle, win32con.SW_SHOW)
            self._showed = self.showed
        else:
            win32gui.ShowWindow(self._handle, win32con.SW_HIDE)
            self._showed = self.showed
    
    @showed.setter
    def showed(self, value):
        raise WindowException("请使用方法修改")

    @class_name.setter
    def class_name(self, value: str):
        """
        设置窗口类名
        """
        raise WindowException("不支持修改窗口类名")
    
    def show(self):
        """
        显示窗口
        """
        win32gui.ShowWindow(self._handle, win32con.SW_SHOW)
        self._showed = self.showed
    
    def hide(self):
        """
        隐藏窗口
        """
        win32gui.ShowWindow(self._handle, win32con.SW_HIDE)
        self._hidden = self.hidden
    
    def normal(self):
        """
        正常显示窗口
        """
        win32gui.ShowWindow(self._handle, win32con.SW_NORMAL)
        self._hidden = self.hidden
    
    def close(self):
        """
        关闭窗口
        """
        win32gui.PostMessage(self._handle, win32con.WM_CLOSE, 0, 0)
    
    def maximize(self):
        """
        最大化窗口
        """
        win32gui.ShowWindow(self._handle, win32con.SW_MAXIMIZE)
        self._showed = self.showed
    
    def minimize(self):
        """
        最小化窗口
        """
        win32gui.ShowWindow(self._handle, win32con.SW_MINIMIZE)
        self._showed = self.showed
    
    def restore(self):
        """
        还原窗口
        """
        win32gui.ShowWindow(self._handle, win32con.SW_RESTORE)
        self._showed = self.showed
    
    def active(self):
        """
        设置窗口为活动窗口
        """
        win32gui.SetForegroundWindow(self._handle)
        self._actived = self.actived
    
    def inactive(self):
        """
        设置窗口为非活动窗口
        """
        win32gui.SetForegroundWindow(0)
        self._actived = self.actived
    

if __name__ == "__main__":
    window = Window.find(68960)
    print(window.title)
