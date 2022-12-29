import random

# Constants
#------------------------------------------

class Game_Config:
    BOARD_HEIGHT = 20 # in terms of num of cubes
    BOARD_WIDTH = 10

#------------------------------------------

class Figure:

    # 0  1  2  3
    # 4  5  6  7
    # 8  9  10 11
    # 12 13 14 15

    types = {
        'I' : [[4, 5, 6, 7], [1, 5, 9, 13]],
        'Z' : [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S' : [[6, 7, 9, 10], [1, 5, 6, 10]],
        'J' : [[1, 5, 6, 7], [1, 2, 5, 9], [5, 6, 7, 11], [3, 7, 11, 10]],
        'L' : [[7, 9, 10, 11], [6, 10, 14, 15], [5, 6, 7, 9], [5, 6, 10, 14]],
        'T' : [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
        'O' : [[1, 2, 5, 6]]
    }

    def __init__(self, type, x=Game_Config.BOARD_WIDTH//2, y=0, rot=0):
        self.x = x
        self.y = y
        self.type = type
        self.rot = rot

    def rotate_clock(self):
        self.rot = (len(self.types[self.type]) + self.rot + 1) % len(self.types[self.type])

    def rotate_cntr_clock(self):
        self.rot = (self.rot - 1) % len(self.types[self.type])

    def matrix(self):
        return self.types[self.type][self.rot]

    def left_edge(self):
        left_most = 3
        for n in self.matrix():
            if n%4 < left_most:
                left_most = n%4
        return left_most

    def right_edge(self):
        right_most = 0
        for n in self.matrix():
            if n%4 > right_most:
                right_most = n%4
        return right_most


class Tetris:

    spoiler = []
    hold_piece = None
    attempt_hold = False

    def __init__(self):
        self.height = Game_Config.BOARD_HEIGHT
        self.width = Game_Config.BOARD_WIDTH
        self.field= [ ['0'] * self.width for i in range(self.height) ]
        self.time_count = 0
        self.lines_count = 0
        self.state = 'start'
        self.figure = None
        self.fill_spoiler()
        self.new_figure()

    def new_figure(self):
        self.figure = Figure(self.spoiler.pop(0))
        if len(self.spoiler) == 4:
            self.fill_spoiler()

    def fill_spoiler(self):
        temp = []
        for key in Figure.types:
            temp.append(key)
        random.shuffle(temp)
        self.spoiler.extend(temp)

    def intersects(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.matrix():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] != '0':
                        return True
        return False

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.matrix():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.type
        self.clear_lines()
        self.attempt_hold = False
        self.new_figure()
        if self.intersects():
            self.state = 'gameover'

    def clear_lines(self):
        lines = 0
        for i in range(0, self.height):
            blanks = 0
            for j in range(self.width):
                if self.field[i][j] == '0':
                    blanks += 1
            if blanks == 0:
                lines += 1
                for a in range(i, 0, -1):
                    for j in range(self.width):
                        self.field[a][j] = self.field[a - 1][j]
        self.lines_count += lines

    def horizontal_edge_guard(self):
        while self.figure.left_edge()+self.figure.x < 0:
                self.move(1)
        while self.figure.right_edge()+self.figure.x >= self.width:
            self.move(-1)


    def hard_drop(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def descend(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def move(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
            
    def rotate(self, dir):
        old_rotation = self.figure.rot
        if dir == 'clock':
            self.figure.rotate_clock()
        else:
            self.figure.rotate_cntr_clock()
        self.horizontal_edge_guard()
        if self.intersects():
            self.figure.rot = old_rotation
            self.horizontal_edge_guard()

    def hold(self):
        if self.attempt_hold == False:
            current_pos_x = self.figure.x
            if self.hold_piece == None:
                self.hold_piece = self.figure
                self.new_figure()
            else:
                old_hold_piece = self.hold_piece
                self.hold_piece = self.figure
                self.figure = old_hold_piece
            self.figure.x, self.figure.y = current_pos_x, 0
            self.horizontal_edge_guard()
            self.attempt_hold = True