import cv2
from basic.realize.base import Realize, RealizeExpection
from typing import Callable
from PIL import Image


class CameraExpection(RealizeExpection):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Camera:
    """
    调用摄像头
    """
    camera_id: int = None  # 当前选中的camera
    _cap: cv2.VideoCapture = None  # 当前摄像头的对象
    
    def __init__(self) -> None:
        """
        初始化, 获取摄像头信息
        """
    
    @property
    def getter(self) -> list[int]:
        """
        获取摄像头列表
        """
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # 尝试打开摄像头
            if not cap.read()[0]:  # 如果摄像头打开失败
                break
            else:
                arr.append(index)
            cap.release()
            index += 1
        return arr
    
    def select(self, _id: int):
        """
        选择某个摄像头
        """
        self.camera_id = _id
    
    def open(self, _id: int = None):
        """
        打开某个摄像头
        """
        if _id is not None:
            self.select(_id)
        self._cap = cv2.VideoCapture(self.camera_id)
        if not self._cap.isOpened():
            raise CameraExpection("摄像头未开启")
    
    def show(self, key: str = "q"):
        """
        显示摄像头的拍摄场景
        """
        if self._cap is None:
            raise CameraExpection("请先打开摄像头再进行操作")
        while True:
            ret, frame = self._cap.read()
            if ret:
                cv2.imshow('摄像头', frame)
            if cv2.waitKey(1) == ord(key):
                break
        return self.image(frame)
    
    def image(self, _img: cv2.Mat = None):
        """
        读取图像为PIL
        """
        if self._cap is None:
            raise CameraExpection("摄像头未开启")
        if _img is None:
            ret, frame = self._cap.read()
            if not ret:
                raise CameraExpection("图像读取失败")
            _img = frame
        rgb_frame = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_frame)
    
    def close(self):
        """
        关闭当前摄像头
        """
        if self._cap is not None:
            self._cap.release()
            self._cap = None
    
    def __del__(self):
        """
        释放所有opencv窗口
        """
        if self._cap is not None:
            self._cap.release()
        cv2.destroyAllWindows()



# while True:
#     # 读取一帧
#     ret, frame = cap.read()
#     # 如果读取帧成功，则显示
#     if ret:
#         cv2.imshow('摄像头', frame)

#     # 按'q'键退出循环
#     if cv2.waitKey(1) == ord('q'):
#         break

if __name__ == "__main__":
    camera = Camera()
    print(camera.getter)
    camera.open(0)
    a = camera.image()
    a.show()
