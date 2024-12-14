"""
所有ui继承此类
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QIcon
from data.config import dp
import sys


class LxzMainWindow(QMainWindow):
    _app: QApplication = None

    def __init__(self, *args, **kwargs) -> None:
        self._app = QApplication(sys.argv)
        super().__init__(*args, **kwargs)
        self.setWindowTitle(dp.qt.default.title)
        self.icon = QIcon(dp.qt.default.icon)
        self.setWindowIcon(self.icon)
        self.layout()
    
    def layout(self):
        """
        绘制ui
        """
    
    def start(self) -> "LxzMainWindow":
        """
        开始绘制
        """
        self.show()
        sys.exit(self._app.exec())
        return self
    
    @property
    def app(self):
        """
        返回应用
        """
        return self._app


if __name__ == "__main__":
    window = LxzMainWindow().start()
    print(window.app)
