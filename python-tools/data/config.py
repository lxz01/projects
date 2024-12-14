from basic.utils import DictPlus as Dp
import os
dp = Dp()
dp.encoding = Dp(
    json = "utf-8"
)
dp.indent = 4
dp.qt = Dp(
    default = Dp(
        title = "Lxz qt",
        icon = os.path.join(os.path.dirname(__file__), "imgs", "bg-ys1.ico"),
        bg = os.path.join(os.path.dirname(__file__), "imgs", "background2.png")  
        )
)

