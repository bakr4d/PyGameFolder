import sys
import pygame
import numpy as np
import copy

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)   # رمادي أفتح شوية عشان يبقى باهت للتعادل
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Proportions
WIDTH = 400
HEIGHT = 400
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# Fonts
FONT_SIZE = 64
SMALL_FONT_SIZE = 32

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
clock = pygame.time.Clock()

board = np.zeros((BOARD_ROWS, BOARD_COLS))

font = pygame.font.Font(None, FONT_SIZE)
small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_board():
    screen.fill(BLACK)
    draw_lines()

def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen, color,
                    (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                     int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                    CIRCLE_RADIUS, CIRCLE_WIDTH
                )
            elif board[row][col] == 2:
                pygame.draw.line(
                    screen, color,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                    (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                    CROSS_WIDTH
                )
                pygame.draw.line(
                    screen, color,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                    (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                    CROSS_WIDTH
                )

def draw_text_center(text, color, font_obj, y_offset=0):
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))

    padding = 10
    bg_rect = pygame.Rect(
        text_rect.left - padding,
        text_rect.top - padding,
        text_rect.width + 2 * padding,
        text_rect.height + 2 * padding
    )
    pygame.draw.rect(screen, BLACK, bg_rect)

    screen.blit(text_surface, text_rect)

def draw_game_over_screen(winner):
    # هنا ما بنرسمش الـ X/O لأننا بالفعل رسمناهم في الـ loop باللون المناسب
    # بس بنرسم النص والتعليمات فقط
    if winner == 1:
        draw_text_center("YOU WON!", GREEN, font, -40)
    elif winner == 2:
        draw_text_center("YOU LOST!", RED, font, -40)
    else:
        draw_text_center("IT'S A TIE!", GRAY, font, -40)

    draw_text_center("Press SPACE to play again", WHITE, small_font, 60)
    draw_text_center("Press ESC to quit", WHITE, small_font, 100)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=None):
    if check_board is None:
        check_board = board
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=None):
    if check_board is None:
        check_board = board

    # Rows
    for row in range(BOARD_ROWS):
        if all(check_board[row][col] == player for col in range(BOARD_COLS)):
            return True
    # Columns
    for col in range(BOARD_COLS):
        if all(check_board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    # Diagonals
    if all(check_board[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(check_board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True

    return False

def minimax(minmax_board, depth, is_maximizing):
    if check_win(2, minmax_board):
        return 10 - depth
    if check_win(1, minmax_board):
        return depth - 10
    if is_board_full(minmax_board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minmax_board[row][col] == 0:
                    minmax_board[row][col] = 2
                    score = minimax(minmax_board, depth + 1, False)
                    minmax_board[row][col] = 0
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minmax_board[row][col] == 0:
                    minmax_board[row][col] = 1
                    score = minimax(minmax_board, depth + 1, True)
                    minmax_board[row][col] = 0
                    best_score = min(best_score, score)
        return best_score

def best_move():
    best_score = -float('inf')
    best_move_pos = (-1, -1)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                temp_board = copy.deepcopy(board)
                temp_board[row][col] = 2
                score = minimax(temp_board, 0, False)
                if score > best_score:
                    best_score = score
                    best_move_pos = (row, col)

    if best_move_pos != (-1, -1):
        mark_square(best_move_pos[0], best_move_pos[1], 2)
        return True
    return False

def restart_game():
    global board
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    draw_board()

# --------- main loop ---------
draw_board()
player = 1
game_over = False
winner = 0
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # حركة اللاعب
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if 0 <= mouseX < BOARD_COLS and 0 <= mouseY < BOARD_ROWS and available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)

                if check_win(player):
                    game_over = True
                    winner = player
                elif is_board_full():
                    game_over = True
                    winner = 0
                else:
                    # دور الـ AI
                    if best_move():
                        if check_win(2):
                            game_over = True
                            winner = 2
                        elif is_board_full():
                            game_over = True
                            winner = 0

        # أزرار الكيبورد
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    restart_game()
                    game_over = False
                    winner = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False
            else:
                if event.key == pygame.K_r:
                    restart_game()
                    game_over = False
                    winner = 0

    if not game_over:
        # أثناء اللعب: القطع والخطوط باللون العادي
        draw_board()
        draw_figures(WHITE)
    else:
        # بعد انتهاء اللعبة: غيّر ألوان القطع والخطوط حسب النتيجة
        if winner == 1:
            draw_board()
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif winner == 2:
            draw_board()
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_board()
            draw_figures(GRAY)   # رمادي باهت للتعادل
            draw_lines(GRAY)

        draw_game_over_screen(winner)

    pygame.display.update()

pygame.quit()
sys.exit()
