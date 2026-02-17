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

if _name_ == "_main_":
    main()