from time import sleep

import pygame
import random
import numpy as np

pygame.init()

# Constants
SCREEN_SIZE = 400
GRID_SIZE = 4
TILE_SIZE = SCREEN_SIZE // GRID_SIZE
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (236, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048 Game')

board = np.zeros((4, 4), dtype=int)

# board[0][0] = 2
# board[0][1] = 0
# board[0][2] = 0
# board[0][3] = 2

board[0][0] = 2
board[1][0] = 2
board[2][0] = 4
board[3][0] = 0
board[0][3] = 4

def add_tile(board):
    print('adding new tile', random.randint(0, 100))
    zeros = np.where(board == 0)

    random.seed = 43

    random_tile = random.randint(0, len(zeros[0]) - 1)

    board[zeros[0][random_tile]][zeros[1][random_tile]] = 2  # random.randint(1, 2) * 2


# add_tile(board)
# add_tile(board)

print(board)

def draw_board(board):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    CELL_SIZE = 100
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            pygame.draw.rect(screen, TILE_COLORS[board[i][j]], (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            font = pygame.font.Font(None, 36)
            text = font.render(str(board[i][j]), True, BLACK)
            text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)


def move_right(board):
    global points
    for i in range(len(board[0])):
        for j in range(len(board[1]) - 1, -1, -1):
            # print(i, j)
            id = j
            for k in range(j + 1, len(board[1])):
                # print(board, '\n', board[i][id], board[i][k], '|', id, k)
                if board[i][id] != 0 and board[i][k] == 0:
                    board[i][id], board[i][k] = board[i][k], board[i][id]
                    # print('#1')
                elif board[i][id] != 0 and board[i][k] == board[i][id]:
                    board[i][id], board[i][k] = 0, board[i][k] * 2
                    points += board[i][k]
                    # print('#2')
                    # print(f'\n{board}')
                    # print('\n------------------------\n')
                    break
                id += 1
            # print(f'\n{board}')
            # print('\n------------------------\n')


def move_left(board):
    global points
    for i in range(len(board[0])):
        for j in range(len(board[1])):
            id = j
            for k in range(j - 1, -1, -1):

                if board[i][id] != 0 and board[i][k] == 0:
                    board[i][id], board[i][k] = board[i][k], board[i][id]

                elif board[i][id] != 0 and board[i][k] == board[i][id]:
                    board[i][id], board[i][k] = 0, board[i][id] * 2
                    points += board[i][k]
                    break

                id -= 1


def move_up(board):
    global points
    for j in range(len(board[1])):
        for i in range(len(board[0])):
            id = i
            for k in range(i - 1, -1, -1):
                if board[id][j] != 0 and board[k][j] == 0:
                    board[id][j], board[k][j] = board[k][j], board[id][j]

                elif board[id][j] != 0 and board[k][j] == board[id][j]:
                    board[id][j], board[k][j] = 0, board[id][j] * 2
                    points += board[k][j]
                    break
                id -= 1


def move_down(board):
    global points
    for j in range(len(board[1])):
        for i in range(len(board[0]) - 1, -1, -1):
            id = i
            for k in range(i + 1, len(board[0])):
                if board[id][j] != 0 and board[k][j] == 0:
                    board[id][j], board[k][j] = board[k][j], board[id][j]

                elif board[id][j] != 0 and board[k][j] == board[id][j]:
                    board[id][j], board[k][j] = 0, board[id][j] * 2
                    points += board[k][j]
                    break
                id += 1


def is_game_over(board):
    if np.count_nonzero(board == 0) == 0:
        for i in range(4):
            for j in range(4):
                if (i > 0 and board[i][j] == board[i - 1][j]) or \
                        (i < 3 and board[i][j] == board[i + 1][j]) or \
                        (j > 0 and board[i][j] == board[i][j - 1]) or \
                        (j < 3 and board[i][j] == board[i][j + 1]):
                    return False
        return True
    return False


points = 0
running = True
while running:
    points_ = points
    board_ = board.copy()
    moved = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_UP:
                move_up(board)
                moved = True
                # add_tile(board)
            elif event.key == pygame.K_DOWN:
                move_down(board)
                moved = True
                # add_tile(board)
            elif event.key == pygame.K_LEFT:
                move_left(board)
                moved = True
                # add_tile(board)
            elif event.key == pygame.K_RIGHT:
                move_right(board)
                moved = True
                # add_tile(board)
    
    if not np.array_equal(board, board_):
        add_tile(board)

    if is_game_over(board):
        print('GOVNO')

    # else:
    #     if moved:
    #         print('GOVNO')
    #         sleep(10)

    screen.fill(BACKGROUND_COLOR)
    draw_board(board)
    pygame.display.flip()

pygame.quit()
