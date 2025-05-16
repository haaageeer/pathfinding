import pygame
import math
from queue import PriorityQueue, Queue, LifoQueue

WIDTH = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, WIDTH))  # size of screen 800x800
pygame.display.set_caption("PATH FINDING Algorithm")  # Title

# defined colors (RGB)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):  # if closed and visited it this spot will color with Red
        return self.color == RED

    def is_open(self):  # if is open sopt is green
        return self.color == GREEN

    def is_barrier(self):  # is a block can not path on it
        return self.color == BLACK

    def is_start(self):  # the start spot
        return self.color == ORANGE

    def is_end(self):  # the end(goal)spot
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):  # make the path
        self.color = PURPLE

    def draw(self, screen):  # draw the spot
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # check DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # check UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # check Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # check LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):  # علشان نمنع المقارنه بين الحاجات اللي مش بتتقارن
        return False

def h(p1, p2):  # to find h(n)
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):  # draw the final path
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithmAStar(draw, grid, start, end):  # A*algorithm
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}  # علشان احط فيه الباس بتاعي
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:  # goal reached
            reconstruct_path(came_from, end, draw)  # draw the final path
            end.make_end()  # علشان اقدر اعرف نقطه النهايه
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # بنعتبر ان المسافه بين اي نود دايما بواحد

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def bfs(draw, grid, start, end): # BFS algorithm
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                queue.put(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def dfs(draw, grid, start, end): # DFS algorithm
    stack = LifoQueue()
    stack.put(start)
    came_from = {}
    visited = {start}

    while not stack.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                stack.put(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows  # تعبر عن Width  بتاع المربع
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot_instance = spot(i, j, gap, rows)
            grid[i].append(spot_instance)
    return grid

def draw_grid(screen, rows, width):  # بيرسم الخطوط اللي بتقسم الشاشه الرمادي
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(screen, GREY, (j * gap, 0), (j * gap, width))

def draw(screen, grid, rows, width):
    screen.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(screen)
    draw_grid(screen, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):  # بتجيب مكان اللي اتضغط عليه
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(screen, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(screen, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # click left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot_instance = grid[row][col]
                if not start and spot_instance != end:
                    start = spot_instance
                    start.make_start()
                elif not end and spot_instance != start:
                    end = spot_instance
                    end.make_end()
                elif spot_instance != end and spot_instance != start:
                    spot_instance.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # click RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot_instance = grid[row][col]
                spot_instance.reset()
                if spot_instance == start:
                    start = None
                elif spot_instance == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: # لو عايز تشتغل A* اضغط space
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithmAStar(lambda: draw(screen, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_b and start and end: # لو عايز BFS press b 
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bfs(lambda: draw(screen, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_d and start and end: # لو عايز DFS press d
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    dfs(lambda: draw(screen, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c: # لو عايز تعيد من جديد اضغط c 
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(screen, WIDTH)
