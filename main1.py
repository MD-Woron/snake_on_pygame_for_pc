"""
Итак, игра "змейка"
1. Создаётся двумерный массив с полем игры
2. Задаются параметры для поля ( случайным образом создаются стены )
3. Каким-то образом по двумерному массиву движется змейка
4. Если змейка попадает на клетку с условным "яблоком", то её длина увеличивается на 1, как и счётчик очков
5. Если змейка "утыкается" в стену или в себя, то очки сбрасываются, а игра откатывается к началу ( без pygame.quit() )

ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ:
1. Автопилот для змейки
2. Змейка в 3 измерениях ( не просто создание 3-дшной змейки, а именно движение змейки в трёх измерениях, от первого/второго лица )
3. Враги змейки ( другие змейки, что угодно другое. Главное чтобы они мешали. Может быть движущиеся стены )
"""


def init_field(sizex, sizey):
    game_field = []
    for index in range(sizey):
        game_field.append(['0'] * sizex)
    return game_field


from random import randint as rnt


def create_walls(game_field, difficult):
    """
    Create walls for zmeyka game on randoms coordinates
    """
    for walls in range(rnt(1, difficult)):
        wall_pos_x = rnt(1, len(game_field) - 2)
        wall_pos_y = rnt(1, len(game_field) - 2)
        flag_0_is_x__1_is_y = rnt(0, 1)
        # cur_wall = (wall_pos_x, wall_pos_y)[flag_0_is_x__1_is_y]
        # wall_long = rnt(cur_wall, len(game_field)-2)
        game_field[wall_pos_x][wall_pos_y] = '1'
        # if flag_0_is_x__1_is_y == 0:
        #     for index in range(wall_pos_x,len(game_field) - 1): # uncomment it if you want line-like walls
        #         game_field[wall_pos_y][index] = '1'
        # else:
        #     for index in range(wall_pos_y, len(game_field) - 1):
        #         game_field[index][wall_pos_x] = '1'
    return game_field


def zm_body_init(game_field, zm_body=1):
    """
    Initialization zmeyka's body and apple. If walls exist around(3x3) zmeyka, then body won't exist
    """
    ay = rnt(0,len(game_field)-1)
    ax = rnt(0,len(game_field[0])-1)
    game_field[ay][ax] = 'apple'
    for row in range(1, len(game_field) - 1):
        for col in range(1, len(game_field) - 1):
            if all(mark == '0' for mark in game_field[col - 1][row - 1:row + 2]) and all(
                    mark == '0' for mark in game_field[col][row - 1:row + 2]) and all(
                mark == '0' for mark in game_field[col + 1][row - 1:row + 2]):
                game_field[col][row] = 'a'
                return game_field, (col,row)
    return game_field


def print_zm(game_field, square_size):
    screen.fill(WHITE)
    wall = pygame.Surface((square_size,square_size))
    wall.fill(WHITE)
    zm = wall.copy()
    zm.fill(BLUE)
    apple = wall.copy()
    apple.fill(RED)
    background = wall.copy()
    background.fill(BLACK)
    for i in range(len(game_field)):
        for j in range(len(game_field[i])):
            if game_field[i][j] == "1":
                screen.blit(wall, (square_size*j,square_size*i))
            if game_field[i][j] == 'a':
                screen.blit(zm,(square_size*j,square_size*i))
            if game_field[i][j] == 'apple':
                screen.blit(apple,(square_size*j,square_size*i))
            if game_field[i][j] == '0':
                screen.blit(background,(square_size*j,square_size*i))
    pygame.display.flip()


def set_size(text, color):
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    return tuple(map(int, text.split()))
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                screen.fill((30, 30, 30))
                text_surface = font.render(text, True, color)
                screen.blit(text_surface, (50, 100))
                pygame.display.flip()


def zm_body_move(game_field,start_move,way, zm_body):
    if start_move:
        flag = False
        # print(zm_body)
        cy,cx = zm_body[0]
        if way == 'w' and cy != 0:
            cy -= 1
        if way == 's' and cy != len(game_field):
            cy += 1
        if way == 'd' and cx != len(game_field[0]):
            cx += 1
        if way == 'a' and cx != 0:
            cx -= 1
        if zm_body[0] == tuple((cy,cx)):
            return [0,0],[0,0]
        if game_field[cy][cx] not in ('1','a'):
            if game_field[cy][cx] == 'apple':
                flag = True
            hvost = zm_body[-1]
            game_field[zm_body[-1][0]][zm_body[-1][1]] = '0'
            zm_body[-1] = (0,0)
            for i in range(len(zm_body)-1):
                zm_body[len(zm_body)-1-i] = zm_body[len(zm_body)-2-i]
            zm_body[0] = tuple((cy,cx))
            if flag:
                zm_body.append(hvost)
                ay = rnt(0, len(game_field) - 1)
                ax = rnt(0, len(game_field[0]) - 1)
                while game_field[ay][ax] in ('1', 'a'):
                    ay = rnt(0, len(game_field) - 1)
                    ax = rnt(0, len(game_field[0]) - 1)
                game_field[ay][ax] = 'apple'
            for i,j in zm_body:
                game_field[i][j] = 'a'
            return game_field, zm_body
        else:
            return 0
    return game_field, zm_body


import pygame
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

WIDTH = screensize[0] // 1.5
HEIGHT = screensize[1] // 1.5
FPS = 60
SCR = (screensize[0] // 2, screensize[1] // 2)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


pygame.init()

font_color = pygame.Color('dodgerblue2')

pygame.display.set_caption('Введите размер поля и максимальное кол-во стен (x y n-1)')
font = pygame.font.SysFont('arial', 64)
text = ''

screen = pygame.display.set_mode((WIDTH, HEIGHT))
field_size = set_size(text, font_color)

square_size = int(((screensize[0] // 2 * screensize[1] // 2) // (field_size[0] * field_size[1]))**0.5)

# print(square_size)
# print(screensize)
#
# print(field_size)

game_field, zm_pos = zm_body_init(create_walls(init_field(*field_size[:2:]), field_size[2]))

# for line in game_field:
#     print(*line)

clock = pygame.time.Clock()
clock.tick(FPS)

way = '1234'
start_move = False
pygame.display.set_caption(f'Длина вашей змейки: 1, чтобы приостановить игру нажмите SPACE')

zm_body = [(zm_pos)]

print_zm(game_field, square_size)
from time import sleep as sp
while True:
    game_field, zm_body = zm_body_move(game_field, start_move, way, zm_body)
    print_zm(game_field, square_size)
    pygame.time.wait(500)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                start_move = True
                way = 'a'
                print_zm(game_field, square_size)
                pygame.display.set_caption(f'Длина вашей змейки: {len(zm_body)}, чтобы приостановить игру нажмите SPACE')
            if event.key == pygame.K_d:
                start_move = True
                way = 'd'
                print_zm(game_field, square_size)
                pygame.display.set_caption(f'Длина вашей змейки: {len(zm_body)}, чтобы приостановить игру нажмите SPACE')
            if event.key == pygame.K_s:
                way = 's'
                start_move = True
                print_zm(game_field, square_size)
                pygame.display.set_caption(f'Длина вашей змейки: {len(zm_body)}, чтобы приостановить игру нажмите SPACE')
            if event.key == pygame.K_w:
                way = 'w'
                start_move = True
                print_zm(game_field, square_size)
                pygame.display.set_caption(f'Длина вашей змейки: {len(zm_body)}, чтобы приостановить игру нажмите SPACE')
            if event.key == pygame.K_SPACE:
                start_move = False
                game_field, zm_body = zm_body_move(game_field, start_move, way, zm_body)
                print_zm(game_field, square_size)
                pygame.display.set_caption('Игра приостановлена. Нажмите W/A/S/D чтобы продолжить')

