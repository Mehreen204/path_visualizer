import pygame

# --- Constants ---
WIDTH, HEIGHT = 700, 700
ROWS = 10
GRID_SIZE = WIDTH // ROWS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

class Node:
    def _init_(self, row, col):
        self.row, self.col = row, col
        self.x = col * GRID_SIZE
        self.y = row * GRID_SIZE
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(win, BLACK, (self.x, self.y, GRID_SIZE, GRID_SIZE), 1)

def make_grid():
    return [[Node(r, c) for c in range(ROWS)] for r in range(ROWS)]

def draw_window(win, grid):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    pygame.display.update()

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")

    grid = make_grid()
    start = None
    target = None

    run = True
    while run:
        draw_window(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
                node = grid[row][col]

                if not start:
                    start = node
                    start.color = GREEN
                elif not target:
                    target = node
                    target.color = RED
                else:
                    node.color = GREY

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    target = None
                    grid = make_grid()

    pygame.quit()
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


Add parent + hashing in Node:

self.parent = None

def _eq_(self, other):
    return isinstance(other, Node) and self.row == other.row and self.col == other.col

def _hash_(self):
    return hash((self.row, self.col))


Add neighbor directions:

DIRECTIONS = [(-1,0),(0,1),(1,0),(0,-1)]


Add BFS:

import collections

def get_neighbors(node, grid):
    neighbors = []
    for dr, dc in DIRECTIONS:
        r, c = node.row + dr, node.col + dc
        if 0 <= r < ROWS and 0 <= c < ROWS:
            if grid[r][c].color != GREY:
                neighbors.append(grid[r][c])
    return neighbors

def reconstruct_path(draw_func, end):
    current = end
    while current.parent:
        current = current.parent
        if current.color not in (GREEN, RED):
            current.color = BLUE
        draw_func()
        pygame.time.delay(20)

def bfs(draw_func, start, target, grid):
    queue = collections.deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == target:
            reconstruct_path(draw_func, target)
            return True

        if current != start:
            current.color = YELLOW

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                neighbor.parent = current
                visited.add(neighbor)
                queue.append(neighbor)

        draw_func()
        pygame.time.delay(10)


Trigger BFS with:

if event.key == pygame.K_SPACE:
    bfs(lambda: draw_window(win, grid), start, target, grid)
Add DFS:

def dfs(draw_func, start, target, grid):
    stack = [start]
    visited = {start}

    while stack:
        current = stack.pop()

        if current == target:
            reconstruct_path(draw_func, target)
            return True

        if current != start:
            current.color = YELLOW

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                neighbor.parent = current
                visited.add(neighbor)
                stack.append(neighbor)

        draw_func()
        pygame.time.delay(10)


Add DLS:

def dls(draw_func, start, target, grid, limit):
    def recursive(node, depth, visited):
        if node == target:
            return True
        if depth <= 0:
            return False

        visited.add(node)
        if node != start:
            node.color = YELLOW

        for neighbor in get_neighbors(node, grid):
            if neighbor not in visited:
                neighbor.parent = node
                if recursive(neighbor, depth - 1, visited):
                    return True

        return False

    return recursive(start, limit, set())


Add keys:

elif event.key == pygame.K_d:
    dfs(...)
elif event.key == pygame.K_l:
    dls(..., limit=10)
if _name_ == "_main_":
    main()