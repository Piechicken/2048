import pygame
import random
import copy
import sys
import math
import time
import pickle

# Configuration
SIZE = 4
WIDTH, HEIGHT = 500, 650
TILE_SIZE = 100
TILE_MARGIN = 10
FONT_SIZE = 40
SAVE_FILE = "save2048.pkl"

# Colors
BACKGROUND_COLOR = (250, 248, 239)
GRID_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (237, 194, 46),
    8192: (237, 194, 46),
}

# Game Logic
class Game2048:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_tile()
        self.add_tile()

    def get_empty_cells(self):
        return [(i, j) for i in range(SIZE) for j in range(SIZE) if self.grid[i][j] == 0]

    def add_tile(self):
        empty = self.get_empty_cells()
        if empty:
            i, j = random.choice(empty)
            self.grid[i][j] = 4 if random.random() < 0.1 else 2

    def move(self, direction):
        original_grid = copy.deepcopy(self.grid)
        if direction == 0:
            self.grid = self.transpose(self.merge_and_slide(self.transpose(self.grid)))
        elif direction == 1:
            self.grid = self.reverse(self.merge_and_slide(self.reverse(self.grid)))
        elif direction == 2:
            temp = self.reverse(self.transpose(self.grid))
            self.grid = self.transpose(self.reverse(self.merge_and_slide(temp)))
        elif direction == 3:
            self.grid = self.merge_and_slide(self.grid)
        if self.grid != original_grid:
            self.add_tile()
            return True
        return False

    def merge_and_slide(self, grid):
        new_grid = []
        for row in grid:
            new_row = [i for i in row if i != 0]
            merged_row = []
            i = 0
            while i < len(new_row):
                if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                    merged_val = new_row[i] * 2
                    merged_row.append(merged_val)
                    self.score += merged_val
                    i += 2
                else:
                    merged_row.append(new_row[i])
                    i += 1
            merged_row.extend([0] * (SIZE - len(merged_row)))
            new_grid.append(merged_row)
        return new_grid

    def transpose(self, grid):
        return [list(row) for row in zip(*grid)]

    def reverse(self, grid):
        return [row[::-1] for row in grid]

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for i in range(SIZE):
            for j in range(SIZE):
                if j < SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return True
                if i < SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return True
        return False

    def is_game_over(self):
        return not self.can_move()

# AI
class AIPlayer:
    def __init__(self):
        matrix = [[13,12,11,10],[6,7,8,9],[5,4,3,2],[0,1,1,0]]
        self.WEIGHT_MATRIX = [[4**val for val in row] for row in matrix]
        self.SAMPLE_LIMIT = 6

    def evaluate(self, game):
        grid = game.grid
        empty_cells_bonus = len(game.get_empty_cells()) * 1000
        weighted_sum = sum(grid[i][j] * self.WEIGHT_MATRIX[i][j]
                           for i in range(SIZE) for j in range(SIZE))
        smoothness = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if grid[i][j]:
                    val = math.log2(grid[i][j])
                    if j < SIZE - 1 and grid[i][j+1]:
                        smoothness -= abs(val - math.log2(grid[i][j+1]))
                    if i < SIZE - 1 and grid[i+1][j]:
                        smoothness -= abs(val - math.log2(grid[i+1][j]))
        return weighted_sum + empty_cells_bonus + smoothness * 10

    def search(self, game_state, depth, is_player_turn):
        if depth == 0 or game_state.is_game_over():
            return self.evaluate(game_state)
        if is_player_turn:
            best_score = -float('inf')
            for move in range(4):
                game_copy = copy.deepcopy(game_state)
                if game_copy.move(move):
                    score = self.search(game_copy, depth - 1, False)
                    best_score = max(best_score, score)
            return best_score
        else:
            empty_cells = game_state.get_empty_cells()
            if not empty_cells:
                return self.evaluate(game_state)
            if len(empty_cells) > self.SAMPLE_LIMIT:
                empty_cells = random.sample(empty_cells, self.SAMPLE_LIMIT)
            total_score = 0
            for i, j in empty_cells:
                for val, prob in [(2, 0.9), (4, 0.1)]:
                    game_copy = copy.deepcopy(game_state)
                    game_copy.grid[i][j] = val
                    total_score += prob * self.search(game_copy, depth - 1, True)
            return total_score / len(empty_cells)

    def get_best_move(self, game):
        best_score = -float('inf')
        best_move = None
        depth = 3 if len(game.get_empty_cells()) > 5 else 4
        for move in range(4):
            game_copy = copy.deepcopy(game)
            if game_copy.move(move):
                score = self.search(game_copy, depth, False)
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move if best_move is not None else random.randint(0, 3)

# UI
def draw(screen, font, game, message, message_time):
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, GRID_COLOR, (0, 0, WIDTH, 100))
    score_text = font.render(f"Score: {game.score}", True, BACKGROUND_COLOR)
    screen.blit(score_text, (20, 30))
    title_text = pygame.font.SysFont("arial", 50, bold=True).render("2048", True, (119, 110, 101))
    screen.blit(title_text, (WIDTH - 120, 20))

    for i in range(SIZE):
        for j in range(SIZE):
            value = game.grid[i][j]
            rect = pygame.Rect(j * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN * 2,
                               i * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN * 2 + 100,
                               TILE_SIZE, TILE_SIZE)
            tile_color = TILE_COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(screen, tile_color, rect, border_radius=6)
            if value:
                text_color = (119, 110, 101) if value <= 4 else (249, 246, 242)
                text_size = FONT_SIZE if value < 1000 else FONT_SIZE - 10
                current_font = pygame.font.SysFont("arial", text_size, bold=True)
                text = current_font.render(str(value), True, text_color)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    # Save / Load buttons
    save_btn = pygame.Rect(30, HEIGHT - 45, 100, 30)
    load_btn = pygame.Rect(WIDTH - 130, HEIGHT - 45, 100, 30)
    pygame.draw.rect(screen, (119, 110, 101), save_btn, border_radius=6)
    pygame.draw.rect(screen, (119, 110, 101), load_btn, border_radius=6)

    save_text = font.render("Save", True, (255, 255, 255))
    load_text = font.render("Load", True, (255, 255, 255))
    screen.blit(save_text, save_text.get_rect(center=save_btn.center))
    screen.blit(load_text, load_text.get_rect(center=load_btn.center))

    # Message display
    if time.time() - message_time < 0.5:
        msg = font.render(message, True, (255, 0, 0))
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT - 80)))

    if game.is_game_over():
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((238, 228, 218, 200))
        screen.blit(overlay, (0, 0))
        game_over_text = pygame.font.SysFont("arial", 60, bold=True).render("GAME OVER", True, (119, 110, 101))
        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
        final_score = font.render(f"Final Score: {game.score}", True, (119, 110, 101))
        screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    pygame.display.flip()

# Save/Load
def save_progress(game):
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump((game.grid, game.score), f)
    return "Save successful"

def load_progress():
    try:
        with open(SAVE_FILE, 'rb') as f:
            grid, score = pickle.load(f)
        g = Game2048()
        g.grid, g.score = grid, score
        return g, "Load successful"
    except:
        return Game2048(), "No save found"

# Load or New Game Prompt
def prompt_load_or_new(screen, font, clock):
    load_btn = pygame.Rect((WIDTH//2 - 120, HEIGHT//2 - 25), (100, 50))
    new_btn = pygame.Rect((WIDTH//2 + 20, HEIGHT//2 - 25), (100, 50))
    while True:
        screen.fill(BACKGROUND_COLOR)
        title = pygame.font.SysFont("arial", 50, True).render("2048", True, (119,110,101))
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))
        pygame.draw.rect(screen, (119,110,101), load_btn, border_radius=8)
        pygame.draw.rect(screen, (119,110,101), new_btn, border_radius=8)
        load_text = font.render("Load", True, (255,255,255))
        new_text = font.render("New", True, (255,255,255))
        screen.blit(load_text, load_text.get_rect(center=load_btn.center))
        screen.blit(new_text, new_text.get_rect(center=new_btn.center))
        pygame.display.flip()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if load_btn.collidepoint(event.pos):
                    return True
                elif new_btn.collidepoint(event.pos):
                    return False

# Main
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 AI Player")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", FONT_SIZE, bold=True)
    if prompt_load_or_new(screen, font, clock):
        game, msg = load_progress()
    else:
        game = Game2048()
        msg = "New game started"
    ai_player = AIPlayer()
    message = msg
    message_time = time.time()
    running = True
    ai_play = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if pygame.Rect(30, HEIGHT - 45, 100, 30).collidepoint(mx, my):
                    message = save_progress(game)
                    message_time = time.time()
                elif pygame.Rect(WIDTH - 130, HEIGHT - 45, 100, 30).collidepoint(mx, my):
                    game, message = load_progress()
                    message_time = time.time()
        if ai_play and not game.is_game_over():
            direction = ai_player.get_best_move(game)
            if direction is not None:
                game.move(direction)
        draw(screen, font, game, message, message_time)
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
