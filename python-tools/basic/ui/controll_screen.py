from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QLabel
from PySide6.QtGui import QPixmap, QIcon, QPalette, QColor, QPainter, QFont, QContextMenuEvent, QAction
from PySide6.QtCore import Qt, QModelIndex, QRect
from PySide6.QtWidgets import QListWidgetItem, QStyleOptionViewItem, QStyle, QMenu
import os

# 自定义对象类
class Picture:
    """
    初始化方法。
    
    :param _icon: 图标文件的路径。
    :type _icon: str
    :param _remark: 图标的备注信息, 默认为None。
    :type _remark: str, optional
    :ivar remark: 图标的备注信息。
    :ivar icon: 图标文件的路径。
    :ivar father: 图标文件所在目录的名称。
    :ivar name: 图标文件的名称（不包括扩展名）。
    :ivar type: 图标文件的扩展名。
    """
    def __init__(self, _icon: str, _remark: str = None):
        self.remark = _remark
        self.icon = _icon
        self.father = os.path.basename(os.path.dirname(os.path.abspath(_icon)))
        self.name = os.path.splitext(os.path.basename(_icon))[0]
        self.type = os.path.splitext(os.path.basename(_icon))[1]

# 自定义QListWidgetItem
class PictureItem(QListWidgetItem):
    def __init__(self, picture: Picture, parent=None):
        super().__init__(parent)
        self.custom_object = picture
        self.setIcon(QIcon(self.custom_object.icon))
        if picture.remark is None:
            self.setText(f"[{self.custom_object.type}]{self.custom_object.name} |{self.custom_object.father}")
        else:
            self.setText(f"[{self.custom_object.type}]{self.custom_object.remark} |{self.custom_object.father}")


class PictureLabel(QLabel):

    def __init__(self, control: "ControlScreen", parent=None):
        super().__init__(parent)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignCenter)
        self.control = control
    
    def contextMenuEvent(self, ev: QContextMenuEvent) -> None:
        if self.control.index_picture is not None:
            menu = QMenu(self)
            action = QAction("查看", self)
            a2 = QAction("打开", self)
            menu.addAction(action)
            menu.addAction(a2)
            menu.exec(ev.globalPos())


class ControlScreen(QWidget):
    index_picture: Picture = None

    def __init__(self):
        # ... 省略其他代码 ...
        super().__init__()

        # 设置窗口标题和图标
        self.setWindowTitle("lxz 控制器")
        self.setWindowIcon(QIcon("./python-tools/data/imgs/2x.ico"))

        # 设置窗口背景色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FFEFFC"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # 创建布局
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.pic_listbox = QListWidget()
        self.text_edit = QTextEdit()
        self.label = PictureLabel(self)

        # 设置左侧部件的最小宽度和高度比例
        self.pic_listbox.setMinimumWidth(200)
        self.text_edit.setMinimumWidth(200)
        self.label.setMinimumWidth(200)
        self.text_edit.setMaximumWidth(200)
        self.pic_listbox.setMaximumWidth(200)
        self.pic_listbox.setMinimumHeight(100)
        self.text_edit.setMinimumHeight(50)
        self.label.setMinimumHeight(150)
        self.text_edit.setMaximumHeight(100)

        # 添加部件到左侧布局
        left_layout.addWidget(self.pic_listbox)
        left_layout.addWidget(self.text_edit)  # 修正这里

        # 添加部件到右侧布局
        right_layout.addWidget(self.label, 1)

        # 将左右布局添加到主布局
        main_layout.addLayout(left_layout, 1)  # 左小右大
        main_layout.addLayout(right_layout, 2)

        # 设置主布局
        self.setLayout(main_layout)

        # 添加自定义对象到list_widget
        self.add(Picture("./python-tools/data/imgs/background2.png"))
        self.add(Picture("./python-tools/data/imgs/background3.png"))
        if self.pic_listbox.count() > 0:
            self.pic_listbox.setCurrentRow(0)
        self.pic_listbox.clicked.connect(self.win_change)
        

    def add(self, picture: Picture):
        if os.path.isfile(picture.icon):
            item = PictureItem(picture)
            self.pic_listbox.addItem(item)
    
    def win_change(self, current: QModelIndex):
        if current.isValid():
            item = self.pic_listbox.itemFromIndex(current)
            if item is not None:
                picture = item.custom_object
                self.picture(picture)

    # ... 省略其他代码 ...
    def picture(self, _picture: Picture):
        # 加载图片
        self.index_picture = _picture
        pixmap = QPixmap(_picture.icon)
        self.label.setPixmap(pixmap)

        # 根据图片大小修改窗口大小
        window_width = pixmap.width() + 20  # 加上一些边距
        window_height = pixmap.height() + 20  # 加上一些边距
        self.setFixedSize(window_width, window_height)
        self.edit(
            f"name: {_picture.name}\n" \
            f"path: {_picture.icon}\n" \
            f"remark: {_picture.remark}\n"
        )
    
    def edit(self, text: str, delete: bool = True):
        """
        编辑文本框内容。
        """
        if delete:
            self.text_edit.clear()
        self.text_edit.append(text)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ControlScreen()
    window.show()
    sys.exit(app.exec())

