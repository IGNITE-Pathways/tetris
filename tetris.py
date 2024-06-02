import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 600
block_size = 30

# Define shapes
shapes = [
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1], [1, 1]],       # O
    [[1, 1, 1, 1]],         # I
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]], # Z
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

# Colors
colors = [
    (0, 255, 255), # Cyan
    (255, 255, 0), # Yellow
    (0, 0, 255),   # Blue
    (255, 165, 0), # Orange
    (0, 255, 0),   # Green
    (255, 0, 0),   # Red
    (128, 0, 128)  # Purple
]

# Game variables
grid = [[0 for x in range(screen_width // block_size)] for y in range(screen_height // block_size)]
clock = pygame.time.Clock()
fall_time = 0

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.color = colors[shapes.index(shape)]
        self.x = screen_width // block_size // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def collision(self, dx, dy, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and (
                    x + self.x + dx < 0 or
                    x + self.x + dx >= len(grid[0]) or
                    y + self.y + dy >= len(grid) or
                    grid[y + self.y + dy][x + self.x + dx]
                ):
                    return True
        return False

    def lock(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[y + self.y][x + self.x] = self.color

def create_grid(locked_positions):
    grid = [[0 for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]
    for y, row in enumerate(locked_positions):
        for x, cell in enumerate(row):
            if cell:
                grid[y][x] = cell
    return grid

def clear_rows(grid, locked_positions):
    cleared = 0
    full_rows = []
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        if 0 not in row:
            cleared += 1
            full_rows.append(y)

    # Animate row clearing
    if full_rows:
        for row in full_rows:
            for x in range(len(grid[row])):
                grid[row][x] = (255, 255, 255)  # Highlight with white color
        draw_grid(screen, grid)
        pygame.display.update()
        pygame.time.delay(300)

    for row in full_rows:
        for move_y in range(row, 0, -1):
            for x in range(len(grid[move_y])):
                grid[move_y][x] = grid[move_y - 1][x]
                locked_positions[move_y][x] = locked_positions[move_y - 1][x]
        grid[0] = [0 for _ in range(screen_width // block_size)]
        locked_positions[0] = [0 for _ in range(screen_width // block_size)]
    return cleared

def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = cell if isinstance(cell, tuple) else (0, 0, 0)
            pygame.draw.rect(surface, color, (x * block_size, y * block_size, block_size, block_size), 0)
            pygame.draw.rect(surface, (128, 128, 128), (x * block_size, y * block_size, block_size, block_size), 1)

def main():
    global grid
    locked_positions = [[0 for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]
    current_piece = Piece(random.choice(shapes))
    next_piece = Piece(random.choice(shapes))
    run = True
    fall_speed = 0.27
    fall_time = 0
    
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            if not current_piece.collision(0, 1, grid):
                current_piece.y += 1
            else:
                current_piece.lock(locked_positions)
                current_piece = next_piece
                next_piece = Piece(random.choice(shapes))
                if current_piece.collision(0, 0, locked_positions):
                    run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not current_piece.collision(-1, 0, grid):
                    current_piece.x -= 1
                if event.key == pygame.K_RIGHT and not current_piece.collision(1, 0, grid):
                    current_piece.x += 1
                if event.key == pygame.K_DOWN and not current_piece.collision(0, 1, grid):
                    current_piece.y += 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if current_piece.collision(0, 0, grid):
                        for _ in range(3):
                            current_piece.rotate()

        draw_grid(screen, grid)
        for y, row in enumerate(current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_piece.color, (current_piece.x * block_size + x * block_size, current_piece.y * block_size + y * block_size, block_size, block_size), 0)
        pygame.display.update()
        cleared = clear_rows(grid, locked_positions)

    pygame.quit()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")
main()
