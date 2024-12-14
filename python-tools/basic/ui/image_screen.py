from basic.ui.base import LxzMainWindow
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from data.config import dp
from PySide6.QtCore import Qt


class ImageShow(LxzMainWindow):
    """
    继承此类可以自定义其余部分的大小等
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def layout(self):
        self.l_ = QVBoxLayout()
        self.label = QLabel("hello")
        self.label.setPixmap(QPixmap(dp.qt.default.bg))
        self.l_.addWidget(self.label)
        self.setLayout(self.l_)
        print(1)


if __name__ == "__main__":
    ImageShow().start()
