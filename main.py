import pygame
import numpy as np
import random

def checkwall(maze, direction, row, col):
    d_row, d_col = direction
    if d_row == 0:
        return maze[row - 1][col] == 1 and maze[row + 1][col] == 1 and maze[row][col + d_col] == 1
    else:
        return maze[row][col - 1] == 1 and maze[row][col + 1] == 1 and maze[row + d_row][col] == 1


def generate_maze_dfs(maze, start_row, start_col, end_row, end_col):
    maze[start_row][start_col] = 0
    rows, cols = len(maze), len(maze[0])
    stack = [(start_row, start_col, 1)]
    endpoints = []
    ahard = []
    # 增加开始前进时向下移动的概率选择方向时前进方向上的概率
    ahard += [(0, 1)] * 3
    while stack:
        row, col, depth = stack[-1]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        directions += ahard
        random.shuffle(directions)
        found = False
        for direction in directions:
            d_row, d_col = direction
            new_row, new_col = row + d_row, col + d_col
            if 0 < new_row < rows - 1 and 0 < new_col < cols - 1 \
                    and maze[new_row][new_col] == 1 \
                    and checkwall(maze, direction, new_row, new_col):
                # 增加下一次选择方向时前进方向上的概率
                ahard = []
                ahard += [direction] * 3
                maze[new_row][new_col] = 0
                stack.append((new_row, new_col,len(stack)))
                found = True
                break
        if not found:
            endpoints.append(stack.pop())
    return endpoints

# 迷宫大小
maze_rows = 40
maze_cols = 40

# 创建一个迷宫结构
maze = np.ones((maze_rows, maze_cols), dtype=int)
# 创建迷雾
dense_fog = np.ones((maze_rows, maze_cols), dtype=int)

# 随机生成迷宫结构
endpoints = generate_maze_dfs(maze, 1, 1, maze_rows - 2, maze_cols - 2)
endpoints = sorted(endpoints, key=lambda x: x[2])

# 墙壁数组
mazewall = maze.copy()


print(maze)
print(mazewall)
print(endpoints)
# 设置起点和终点的位置，用2和3表示
# maze[1, 1] = 2
# maze[endpoints[len(endpoints) - 1][0], endpoints[len(endpoints) - 1][1]] = 3
# 起始点位置
startpoint = (1, 1)
# 结束点位置
endpoint = endpoints[-1]
# 小人的位置
player = (1, 1)
# 最佳步数
best_step_count = endpoint[2]
# 当前步数
step_count = 0

# 定义颜色
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

# 每个绘制区域的大小
CELL_WIDTH = 10
CELL_HEIGHT = 10
# 下面信息框参数
INFO_VIEW_HEIGHT = 60
INFO_CELL_WIDTH = 90
INFO_CELL_HEIGHT = 30
# 圆球直径
RADIUS = 4
# 刷新间隔 ms
DELAY = 50
#视野范围
VIEW_RANG = 2

# 设置移动速度和计时器
move_speed = 1000
last_move_time = 0

# 初始化pygame
pygame.init()
pygame.font.init()

font = pygame.font.Font('gb.ttc', 10)

# 设置窗口大小
screen = pygame.display.set_mode((maze_rows * CELL_WIDTH, maze_cols * CELL_HEIGHT + INFO_VIEW_HEIGHT))

# 设置窗口标题
pygame.display.set_caption("Maze")

# 设置游戏循环标志
done = False

# 游戏循环
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            # 根据按键状态移动小人
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > move_speed:
                # 根据按键状态移动小人
                if event.key == pygame.K_LEFT and player[1] > 0 and maze[player[0]][player[1] - 1] == 0:
                        player = (player[0], player[1] - 1)
                        step_count += 1
                elif event.key == pygame.K_RIGHT and player[1] < maze_rows - 1 and maze[player[0]][player[1] + 1] == 0:
                        player = (player[0], player[1] + 1)
                        step_count += 1
                elif event.key == pygame.K_UP and player[0] > 0 and maze[player[0] - 1][player[1]] == 0:
                        player = (player[0] - 1, player[1])
                        step_count += 1
                elif event.key == pygame.K_DOWN and player[0] < maze_cols - 1 and maze[player[0] + 1][player[1]] == 0:
                        player = (player[0] + 1, player[1])
                        step_count += 1
    # 重新计算视野 以小人为中心3格范围内为可视范围
    for i in range(-VIEW_RANG, VIEW_RANG + 1):
        for j in range(-VIEW_RANG, VIEW_RANG + 1):
            new_row, new_col = player[0] + i, player[1] + j
            if i ** 2 + j ** 2 <= VIEW_RANG ** 2 and 0 < new_row < maze_rows - 1 and 0 < new_col < maze_cols - 1:
                dense_fog[new_row][new_col] = 0

    # 绘制迷宫
    for row in range(maze_rows):
        for col in range(maze_cols):
            rect = pygame.Rect(col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            if dense_fog[row][col] == 1:
                pygame.draw.rect(screen, GRAY, rect)
            elif maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
    # 画起点
    pygame.draw.circle(screen, (255, 0, 0), (startpoint[1] * CELL_WIDTH + CELL_WIDTH / 2, startpoint[0] * CELL_HEIGHT + CELL_HEIGHT / 2), RADIUS)
    # 画终点
    pygame.draw.circle(screen, (0, 255, 0), (endpoint[1]*CELL_WIDTH+CELL_WIDTH/2, endpoint[0]*CELL_HEIGHT+CELL_HEIGHT/2), RADIUS)
    # 画小人
    pygame.draw.circle(screen, (0, 0, 255), (player[1]*CELL_WIDTH+CELL_WIDTH/2, player[0]*CELL_HEIGHT+CELL_HEIGHT/2), RADIUS)

    rect = pygame.Rect(0, maze_cols * CELL_HEIGHT, maze_cols * CELL_WIDTH, maze_cols * CELL_HEIGHT + INFO_VIEW_HEIGHT)
    pygame.draw.rect(screen, WHITE, rect)

    # 展示最好步数
    best_step_count_rect = pygame.Rect(0, maze_cols * CELL_HEIGHT, INFO_CELL_WIDTH, INFO_CELL_HEIGHT)
    screen.blit(font.render('最佳成绩：' + str(best_step_count), True, BLACK), (best_step_count_rect[0], best_step_count_rect.center[1]))
    # 展示当前步数
    step_count_rect = pygame.Rect(INFO_CELL_WIDTH, maze_cols * CELL_HEIGHT, INFO_CELL_WIDTH, INFO_CELL_HEIGHT)
    screen.blit(font.render('当前步数：' + str(step_count), True, BLACK), (step_count_rect[0], step_count_rect.center[1]))

    # 更新屏幕
    pygame.display.flip()
    pygame.time.delay(DELAY)

# 退出pygame
pygame.quit()
