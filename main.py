from random import shuffle

from logics import *
from constants import *
from database import *
import pygame
import sys

TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')


# Диалоговое окно программы (Размеры и расположение)
def draw_interface(score, delta=0):
    result = get_best()
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont('stxingkai', 70)
    font_score = pygame.font.SysFont('simsun', 48)
    font_delta = pygame.font.SysFont('simsun', 32)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_top = font_score.render('Top 3:', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
    for i in range(len(result)):
        text_top_value = font_delta.render(f'{i + 1}. {result[i][0]}: {result[i][1]}', True, COLOR_TEXT)
        screen.blit(text_top_value, (270, 32 + i * 20))
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (175, 35))
    screen.blit(text_top, (270, 1))

    if delta > 0:
        text_delta = font_delta.render(f'+{delta}', True, COLOR_TEXT)
        screen.blit(text_delta, (170, 85))

    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))


def get_empty_list(mas):
    empty = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                num = get_number_from_index(i, j)
                empty.append(num)
    return empty


def draw_intro():
    global USERNAME
    img2048 = pygame.image.load('2048_logo.svg.png')
    font = pygame.font.SysFont('stxingkai', 70)
    text_welcome = font.render('Welcome!', True, WHITE)
    name = 'Enter your name'
    # len_name_error_txt = font.render('Name length should exceed 2 letters', True, WHITE)
    is_find_name = False

    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Enter your name':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if len(name) > 2:
                        USERNAME = name
                        is_find_name = True
                        break
                    # else:
                    #     screen.blit(len_name_error_txt, (10, 300))
                    #     pygame.display.update()

        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [145, 10])
        screen.blit(text_welcome, (155, 220))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)


def game_loop():
    global score, mas, delta
    draw_interface(score)
    pygame.display.update()
    is_mas_move = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_move = swipe(mas, 'LEFT')
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_move = swipe(mas, 'RIGHT')
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = swipe(mas, 'UP')
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = swipe(mas, 'DOWN')
                score += delta
                if is_zero_in_mas(mas) and is_mas_move:
                    empty = get_empty_list(mas)
                    shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_or_4(mas, x, y)
                    print(f'Мы заполнили элемент под номерсм {random_num}')
                    is_mas_move = False
            draw_interface(score, delta)
            pygame.display.update()


def draw_game_over():
    global USERNAME, score, mas
    write_scores(USERNAME, score)
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont('stxingkai', 70)
    font_score = pygame.font.SysFont('simsun', 48)
    font_smaller = pygame.font.SysFont('simsun', 30)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
    text_restart = font_smaller.render('To play again press Space button', True, COLOR_TEXT)
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (175, 35))
    mas_game_over = [['G', 'A', 'M', 'E'], ['O', 'V', 'E', 'R']]
    is_new_game_pressed = False
    while not is_new_game_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_new_game_pressed = True
                    init_const()
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    USERNAME = None
                    is_new_game_pressed = True
                    init_const()

        for row in range(len(mas_game_over)):
            for column in range(4):
                value = mas_game_over[row][column]
                text = font.render(f'{value}', True, RED)
                w = column * SIZE_BLOCK + (column + 1) * MARGIN
                h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
                pygame.draw.rect(screen, BLACK, (w, h, SIZE_BLOCK, SIZE_BLOCK))

                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2


                screen.blit(text, (text_x, text_y))

                screen.blit(text_restart, (70, 500))
                pygame.display.update()
    screen.fill(BLACK)


while True:
    if USERNAME is None:
        draw_intro()

    game_loop()

    draw_game_over()
