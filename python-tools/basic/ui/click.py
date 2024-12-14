import pygame
import sys
from datetime import datetime
import ctypes

# 初始化pygame
pygame.init()

# 设置窗口大小和标题
width, height = 400, 400
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("时钟")

# 设置时钟颜色
clock_color = (255, 255, 255)
hand_color = (255, 255, 0)

# 设置时钟轮盘大小和位置
clock_radius = 150
clock_x = width // 2
clock_y = height // 2

# 设置时钟指针长度和宽度
hour_hand_length = 60
minute_hand_length = 80
second_hand_length = 90
hand_width = 4

# 设置时钟刻度
hour_marks = 12
minute_marks = 60
# # 获取窗口句柄
# hwnd = pygame.display.get_wm_info()["window"]

# # 设置窗口置顶
# ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0008)
# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 清屏
    screen.fill((0, 0, 0, 0))

    # 绘制时钟轮盘
    pygame.draw.circle(screen, clock_color, (clock_x, clock_y), clock_radius, 2)

    # 绘制时钟刻度
    # 绘制时钟刻度
    for i in range(hour_marks):
        angle = i * (360 / hour_marks) - 90
        if i % 3 == 0:  # 0、3、6、9四个小时的刻度
            start_pos = pygame.math.Vector2(clock_x, clock_y) + clock_radius * pygame.math.Vector2(1, 0).rotate(angle)
            end_pos = pygame.math.Vector2(clock_x, clock_y) + (clock_radius - 20) * pygame.math.Vector2(1, 0).rotate(angle)
            pygame.draw.line(screen, hand_color, start_pos, end_pos, 3)
        else:
            start_pos = pygame.math.Vector2(clock_x, clock_y) + clock_radius * pygame.math.Vector2(1, 0).rotate(angle)
            end_pos = pygame.math.Vector2(clock_x, clock_y) + (clock_radius - 10) * pygame.math.Vector2(1, 0).rotate(angle)
            pygame.draw.line(screen, hand_color, start_pos, end_pos, 2)

    for i in range(minute_marks):
        angle = i * (360 / minute_marks) - 90
        start_pos = pygame.math.Vector2(clock_x, clock_y) + clock_radius * pygame.math.Vector2(1, 0).rotate(angle)
        end_pos = pygame.math.Vector2(clock_x, clock_y) + (clock_radius - 10) * pygame.math.Vector2(1, 0).rotate(angle)
        pygame.draw.line(screen, clock_color, start_pos, end_pos, 1)

    # 获取当前时间
    now = datetime.now()
    hour = now.hour % 12
    minute = now.minute
    second = now.second

    # 计算角度
    # 计算角度
    # 计算角度
    # 计算角度
    # 计算角度
    hour_angle = ((hour % 12) * 30) + (minute * 0.5) + (second * 0.008333) - 90
    minute_angle = minute * 6 + (second * 0.1) - 90
    second_angle = second * 6 - 90

    # 绘制时钟指针
    pygame.draw.line(screen, hand_color, (clock_x, clock_y),
                     (clock_x + hour_hand_length * pygame.math.Vector2(1, 0).rotate(hour_angle).x,
                      clock_y + hour_hand_length * pygame.math.Vector2(1, 0).rotate(hour_angle).y),
                     hand_width)
    pygame.draw.line(screen, hand_color, (clock_x, clock_y),
                     (clock_x + minute_hand_length * pygame.math.Vector2(1, 0).rotate(minute_angle).x,
                      clock_y + minute_hand_length * pygame.math.Vector2(1, 0).rotate(minute_angle).y),
                     hand_width)
    pygame.draw.line(screen, hand_color, (clock_x, clock_y),
                     (clock_x + second_hand_length * pygame.math.Vector2(1, 0).rotate(second_angle).x,
                      clock_y + second_hand_length * pygame.math.Vector2(1, 0).rotate(second_angle).y),
                     1)

    # 绘制日期时间
    font = pygame.font.Font(None, 36)
    date_time_text = font.render(now.strftime("%Y-%m-%d %H:%M:%S"), True, clock_color)
    text_rect = date_time_text.get_rect(center=(width // 2, clock_y - 40))
    screen.blit(date_time_text, text_rect)

    # 更新屏幕
    pygame.display.flip()

    # 控制刷新频率
    pygame.time.Clock().tick(1)