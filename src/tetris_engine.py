import random

# Constants
#------------------------------------------

class Game_Config:
    BOARD_HEIGHT = 20 # in terms of num of cubes
    BOARD_WIDTH = 10

#------------------------------------------

class Figure:

    types = {
        'I' : [[4, 5, 6, 7], [1, 5, 9, 13]],
        'Z' : [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S' : [[6, 7, 9, 10], [1, 5, 6, 10]],
        'J' : [[0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10], [1, 2, 5, 9]],
        'L' : [[3, 5, 6, 7], [1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11]],
        'T' : [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O' : [[1, 2, 5, 6]]
    }

    def __init__(self, type, x=Game_Config.BOARD_WIDTH//2, y=Game_Config.BOARD_HEIGHT-1, rot=0):
        self.x = x
        self.y = y
        self.type = type
        self.rot = rot

    def rotate_clock(self):
        self.rot = (self.rot + 1) % len(self.types[self.type])

    def rotate_cntr_clock(self):
        self.rot = (self.rot - 1) % len(self.types[self.type])

    def matrix(self):
        return self.types[self.type][self.rot]


class Tetris:

    spoiler = []
    hold_piece = None
    attempt_hold = False
    is_freeze = False

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

    def clear_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == '0':
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.lines_count += lines

    def hard_drop(self):
        while not self.intersects():
            self.figure.y -= 1
        self.figure.y += 1
        self.freeze()

    def descend(self):
        self.figure.y -= 1
        if self.intersects():
            self.figure.y += 1
            self.freeze()

    def freeze(self):
        self.is_freeze = True
        if self.figure.y > 19:
            self.state = 'gameover'
        else:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.figure.matrix():
                        print(i + self.figure.y)
                        print(j + self.figure.x)
                        self.field[i + self.figure.y][j + self.figure.x] = self.figure.type
            self.clear_lines()
            self.new_figure()
            if self.intersects():
                self.state = 'gameover'
        self.is_freeze = False

    def move(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
            
    def rotate(self, dir):
        old_rotation = self.figure.rot
        if dir == 'clock':
                self.figure.rotate_clock
        else:
            self.figure.rotate_cntr_clock
        if self.intersects():
            self.figure.rot = old_rotation

    def hold(self):
        self.attempt_hold = True
        
        if self.hold_piece == None:
            self.hold_piece = self.figure
            self.new_figure()
        else:
            current_pos_x = self.figure.x
            old_hold_piece = self.hold_piece
            self.hold_piece = self.figure
            self.figure = old_hold_piece
            self.figure.x, self.figure.y = current_pos_x, Game_Config.BOARD_HEIGHT-1