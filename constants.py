from random import shuffle
from logics import *


def init_const():
    global score, mas
    mas = [[0 for _ in range(4)] for _ in range(4)]

    empty = get_empty_list(mas)
    shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    mas = insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    mas = insert_2_or_4(mas, x2, y2)
    score = 0

COLOR_TEXT = (255, 127, 0)
COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 130),
    16: (255, 235, 255),
    32: (255, 235, 128),
    64: (255, 235, 0),
    128: (255, 210, 0),
    256: (255, 190, 0),
    512: (255, 170, 0),
    1024: (255, 150, 0),
    2048: (255, 130, 0),
    4096: (255, 100, 0),
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)
RED = (255, 0, 0)
BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 110
USERNAME = None
delta = 0
mas = None
score = None
init_const()