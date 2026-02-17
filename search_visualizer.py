import pygame
import collections
import random
import heapq

# --- Constants & GUI Settings ---
WIDTH, HEIGHT = 700,700
ROWS = 10  # smaller grid for better visualization
GRID_SIZE = WIDTH // ROWS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)    # Start
RED = (255, 0, 0)      # Target
BLUE = (0, 0, 255)     # Path
YELLOW = (255, 255, 0) # BFS/DFS visited
CYAN = (0, 255, 255)   # DLS/IDDFS/BiDir backward visited
GREY = (128, 128, 128) # Obstacle

DYNAMIC_PROBABILITY = 0.02  # dynamic obstacle spawn probability

# Clockwise including diagonals
DIRECTIONS = [
    (-1, 0), (0, 1), (1, 0), (0, -1),
    (1, 1), (-1, -1), (-1, 1), (1, -1)
]

class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.x = col * GRID_SIZE
        self.y = row * GRID_SIZE
        self.color = WHITE
        self.parent = None
        self.cost = 0  # For UCS

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(win, BLACK, (self.x, self.y, GRID_SIZE, GRID_SIZE), 1)

    def reset_pathfinding_color(self):
        if self.color in (YELLOW, BLUE, CYAN):
            self.color = WHITE
        self.parent = None
        self.cost = 0

    def __eq__(self, other):
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

def make_grid():
    return [[Node(r, c) for c in range(ROWS)] for r in range(ROWS)]

def draw_window(win, grid):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    pygame.display.update()

def get_neighbors(node, grid):
    neighbors = []
    for dr, dc in DIRECTIONS:
        r, c = node.row + dr, node.col + dc
        if 0 <= r < ROWS and 0 <= c < ROWS:
            if grid[r][c].color != GREY:
                neighbors.append(grid[r][c])
    return neighbors

def spawn_dynamic_obstacle(grid, start, target):
    if random.random() < DYNAMIC_PROBABILITY:
        r, c = random.randint(0, ROWS-1), random.randint(0, ROWS-1)
        node = grid[r][c]
        if node != start and node != target:
            node.color = GREY

def reconstruct_path(draw_func, end):
    current = end
    while current.parent:
        current = current.parent
        if current.color not in (GREEN, RED):
            current.color = BLUE
        draw_func()
        pygame.time.delay(20)

def bfs(draw_func, start, target, grid):
    container = collections.deque([start])
    visited = {start}

    while container:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        current = container.popleft()
        if current.color == GREY and current != start:
            continue
        if current == target:
            reconstruct_path(draw_func, target)
            return True
        if current != start:
            current.color = YELLOW
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                neighbor.parent = current
                visited.add(neighbor)
                container.append(neighbor)
        spawn_dynamic_obstacle(grid, start, target)
        draw_func()
        pygame.time.delay(10)
    return False

def dfs(draw_func, start, target, grid):
    container = [start]
    visited = {start}

    while container:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        current = container.pop()
        if current.color == GREY and current != start:
            continue
        if current == target:
            reconstruct_path(draw_func, target)
            return True
        if current != start:
            current.color = YELLOW
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                neighbor.parent = current
                visited.add(neighbor)
                container.append(neighbor)
        spawn_dynamic_obstacle(grid, start, target)
        draw_func()
        pygame.time.delay(10)
    return False

def dls(draw_func, start, target, grid, limit):
    def recursive_dls(node, depth, visited):
        if node.color == GREY and node != start:
            return False
        if node == target:
            return True
        if depth <= 0:
            return False
        visited.add(node)
        if node != start:
            node.color = CYAN
        for neighbor in get_neighbors(node, grid):
            if neighbor not in visited:
                neighbor.parent = node
                if recursive_dls(neighbor, depth - 1, visited):
                    return True
        draw_func()
        pygame.time.delay(10)
        return False

    visited = set()
    return recursive_dls(start, limit, visited)

def iddfs(draw_func, start, target, grid, max_depth=20):
    for depth in range(1, max_depth + 1):
        for row in grid:
            for node in row:
                node.reset_pathfinding_color()
        if dls(draw_func, start, target, grid, depth):
            return True
    return False

def ucs(draw_func, start, target, grid):
    pq = []
    count = 0  # tie-breaker for heapq
    heapq.heappush(pq, (0, count, start))
    visited = set()

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        cost, _, current = heapq.heappop(pq)
        if current.color == GREY and current != start:
            continue
        if current == target:
            reconstruct_path(draw_func, target)
            return True
        if current != start:
            current.color = YELLOW
        visited.add(current)

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                neighbor.parent = current
                count += 1
                heapq.heappush(pq, (cost + 1, count, neighbor))  # tie-breaker
        spawn_dynamic_obstacle(grid, start, target)
        draw_func()
        pygame.time.delay(10)
    return False

def bidirectional_search(draw_func, start, target, grid):
    f_queue = collections.deque([start])
    b_queue = collections.deque([target])
    f_visited = {start: None}
    b_visited = {target: None}

    meet_node = None

    while f_queue and b_queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Forward step
        f_current = f_queue.popleft()
        if f_current.color == GREY and f_current != start:
            continue
        if f_current in b_visited:
            meet_node = f_current
            break
        if f_current != start:
            f_current.color = YELLOW
        for neighbor in get_neighbors(f_current, grid):
            if neighbor not in f_visited:
                neighbor.parent = f_current
                f_visited[neighbor] = f_current
                f_queue.append(neighbor)

        # Backward step
        b_current = b_queue.popleft()
        if b_current.color == GREY and b_current != target:
            continue
        if b_current in f_visited:
            meet_node = b_current
            break
        if b_current != target:
            b_current.color = CYAN
        for neighbor in get_neighbors(b_current, grid):
            if neighbor not in b_visited:
                neighbor.parent = b_current
                b_visited[neighbor] = b_current
                b_queue.append(neighbor)

        spawn_dynamic_obstacle(grid, start, target)
        draw_func()
        pygame.time.delay(10)

    if meet_node:
        # reconstruct forward
        current = meet_node
        while current.parent:
            current = current.parent
            if current.color not in (GREEN, RED):
                current.color = BLUE
            draw_func()
            pygame.time.delay(20)
        # reconstruct backward
        current = meet_node
        while current.parent:
            current = current.parent
            if current.color not in (GREEN, RED):
                current.color = BLUE
            draw_func()
            pygame.time.delay(20)
        return True
    return False

# ---------------- Main GUI ---------------- #

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "Pathfinding Visualizer (Space:BFS, D:DFS, L:DLS, I:IDDFS, U:UCS, B:BiDir, C:Clear)"
    )

    grid = make_grid()
    start = None
    target = None

    run = True
    while run:
        draw_window(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
                node = grid[row][col]
                if not start and node != target:
                    start = node
                    start.color = GREEN
                elif not target and node != start:
                    target = node
                    target.color = RED
                elif node != target and node != start:
                    node.color = GREY

            if event.type == pygame.KEYDOWN:
                if start and target:
                    if event.key == pygame.K_SPACE:
                        bfs(lambda: draw_window(win, grid), start, target, grid)
                    elif event.key == pygame.K_d:
                        dfs(lambda: draw_window(win, grid), start, target, grid)
                    elif event.key == pygame.K_l:
                        dls(lambda: draw_window(win, grid), start, target, grid, limit=10)
                    elif event.key == pygame.K_i:
                        iddfs(lambda: draw_window(win, grid), start, target, grid, max_depth=15)
                    elif event.key == pygame.K_u:
                        ucs(lambda: draw_window(win, grid), start, target, grid)
                    elif event.key == pygame.K_b:
                        bidirectional_search(lambda: draw_window(win, grid), start, target, grid)

                if event.key == pygame.K_c:
                    start = None
                    target = None
                    grid = make_grid()

    pygame.quit()


if __name__ == "__main__":
    main()
