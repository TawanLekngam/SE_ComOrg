from random import randint
from time import sleep

from sense_emu import SenseHat

sense = SenseHat()
over = False
pos_x = 2
pos_y = 4

GREEN = (178, 235, 103)
STAR = (247, 220, 143)
BLACK = (0, 0, 0)

matrix = [[BLACK for column in range(8)] for row in range(8)]


def flatten(matrix: list):
    flattened = [pixel for row in matrix for pixel in row]
    return flattened


def gen_pipes(matrix: list):
    for row in matrix:
        row[-1] = GREEN
    gap = randint(1, 6)
    matrix[gap][-1] = BLACK
    matrix[gap - 1][-1] = BLACK
    matrix[gap + 1][-1] = BLACK
    return matrix


def move_pipes(matrix: list):
    for row in matrix:
        for i in range(7):
            row[i] = row[i + 1]
        row[-1] = BLACK
    return matrix


def draw_pilot(event):
    global pos_x
    global pos_y
    global over
    sense.set_pixel(pos_x, pos_y, BLACK)
    if event.action == "pressed":
        if event.direction == "up" and pos_y > 0:
            pos_y -= 1
        elif event.direction == "down" and pos_y < 7:
            pos_y += 1

    sense.set_pixel(pos_x, pos_y, STAR)


def check_collision(matrix):
    if matrix[pos_y][pos_x] == GREEN:
        return True
    return False


sense.stick.direction_any = draw_pilot

while not over:
    matrix = gen_pipes(matrix)
    if check_collision(matrix):
        over = True
    for i in range(4):
        sense.set_pixels(flatten(matrix))
        matrix = move_pipes(matrix)
        sense.set_pixel(pos_x, pos_y, STAR)
        if check_collision(matrix):
            over = True
            break
        sleep(1)

sense.clear()
sense.show_message('You Lose')
