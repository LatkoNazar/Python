import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((900, 900))
board = [['' for _ in range(3)] for _ in range(3)]

def start_menu():
    pygame.init()
    start_window = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Tic-tac-toe")
    icon = pygame.image.load('figures/X_and_O.png')
    pygame.display.set_icon(icon)
    start_window.fill((150, 255, 255))
    first_running = True
    button_rect = pygame.Rect(0, 0, 400, 200)
    button_color = ((150, 255, 255))
    pygame.display.update()
    while first_running:
        pygame.draw.rect(start_window, button_color, button_rect)
        pygame.draw.rect(start_window, (0, 0, 0), button_rect, 5)
        font = pygame.font.SysFont('arial', 150)
        window_text = font.render("PLAY", 1, (0, 0, 0))
        text_position = window_text.get_rect(center=(200, 100))
        start_window.blit(window_text, text_position)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                first_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    first_running = False
                    game_mode()

def draw_board():
    for row in range(1, 3):
        pygame.draw.line(screen, (0,0,255), (0, row * 300), (900, row * 300), 3)
    for col in range(1, 3):
        pygame.draw.line(screen, (0, 0, 255), (col * 300, 0), (col * 300, 900), 3)

def draw_marks(row, col):
    if board[row][col] == 'X':
        image_x = pygame.image.load('figures/X.png')
        rect_x = image_x.get_rect()
        rect_x.topleft = (col * 300, row * 300)
        screen.blit(image_x, rect_x)
    elif board[row][col] == 'O':
        image_circle = pygame.image.load('figures/O_pic.png')
        rect_circle = image_circle.get_rect()
        rect_circle.topleft = (col * 300, row * 300)
        screen.blit(image_circle, rect_circle)

def check_winner(player_turn):
    for row in range(3):
        if all(board[row][col] == player_turn for col in range(3)):
            return True
    for col in range(3):
        if all(board[row][col] == player_turn for row in range(3)):
            return True
    if all(board[i][i] == player_turn for i in range(3)):
        return True
    if all(board[i][2 - i] == player_turn for i in range(3)):
        return True
    return False

def check_draw():
    if all(board[i][j] != '' for i in range(3) for j in range(3)):
        return True

def result(message):
    pygame.init()
    window = pygame.display.set_mode((400, 100))
    pygame.display.set_caption("Result")
    font = pygame.font.SysFont('arial', 55)
    window_text = font.render(message, 1, (0, 0, 0))
    position = window_text.get_rect(center=(200, 50))
    window.fill((150, 255, 255))
    borders = pygame.Rect(0, 0, 400, 100)
    pygame.draw.rect(window, (0, 0, 0), borders, 5)
    window.blit(window_text, position)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
    sys.exit()
        
def game_mode():
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Tic-tac-toe")
    icon = pygame.image.load('figures/X_and_O.png')
    pygame.display.set_icon(icon)
    X = 'X'
    O = 'O'
    result_shown = False
    player_turn = 'X'
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // 300
                row = y // 300
                if board[row][col] == '':
                    board[row][col] = player_turn
                    player_turn = 'O' if player_turn == 'X' else 'X'

        screen.fill((150, 255, 255))
        draw_board()

        for row in range(3):
            for col in range(3):
                if board[row][col] != '':
                    draw_marks(row, col)
        if check_draw():
            message="Draw!"
            game_over = True
        if check_winner(O):
            message="O won!!!"
            game_over = True
        if check_winner(X):
            message="X won!!!"
            game_over = True
        pygame.display.update()

        if game_over == True and not result_shown:
            result(message)
for event_result in pygame.event.get():
    if event_result.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
start_menu()