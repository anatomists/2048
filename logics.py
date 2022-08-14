from random import choice
import copy


rotate_count = {
    "LEFT": 0,
    "UP": 3,
    "RIGHT": 2,
    "DOWN": 1
}


def can_move(mas):
    for i in range(4):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1]:
                return True
    for i in range(3):
        for j in range(4):
            if mas[i][j] == mas[i + 1][j]:
                return True
    return False


def get_number_from_index(i, j):
    return i * 4 + j + 1


def get_index_from_number(num):
    num -= 1
    x, y = num // 4, num % 4
    return x, y


def insert_2_or_4(mas, x, y):
    mas[x][y] = choice((2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
    return mas


def get_empty_list(mas):
    empty = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                num = get_number_from_index(i, j)
                empty.append(num)
    return empty


def is_zero_in_mas(mas):
    for row in mas:
        if 0 in row:
            return True
    return False


def move_left(mas):
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j + 1)
                mas[i].append(0)
    return mas, delta


def rotate_ccw(mas):
    # поворот против часовой стрелки
    new_matrix = [[0] * 4 for i in range(4)]

    for row in range(4):
        for col in range(4):
            new_matrix[col][3 - row] = mas[row][col]
    return new_matrix


def rotate_cw(mas):
    # поворот по часовой стрелке
    for i in range(3):
        mas = rotate_ccw(mas)
    return mas


def swipe(mas, direction):
    # сохраним массив до хода
    origin = copy.deepcopy(mas)

    rotates = rotate_count[direction]

    for i in range(rotates):
        mas = rotate_ccw(mas)

    mas, delta = move_left(mas)

    for i in range(rotates):
        mas = rotate_cw(mas)

    return mas, delta, origin != mas


def is_move_is_possible(mas, direction):
    return mas != swipe(mas, direction)

