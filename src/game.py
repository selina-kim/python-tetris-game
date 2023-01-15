import pyglet
from pyglet.window.key import *
from pyglet.gui.widgets import WidgetBase
from pyglet import resource
from pyglet import font

import os
from tetris_engine import Game_Config
from tetris_engine import Tetris

import keyboard_input

# Constants ----------------------
CUBE_LENGTH = 30
WINDOW_X = 900
WINDOW_Y = 740
WINDOW_MIN_Y = CUBE_LENGTH*(Game_Config.BOARD_HEIGHT+1)
WINDOW_MIN_X = CUBE_LENGTH*(Game_Config.BOARD_WIDTH+2)
#------------------------------------------

workingDir = os.path.dirname( os.path.realpath( __file__ ) )
resource.path = [ os.path.join( workingDir, '../assets/font' ), os.path.join( workingDir, '../assets/img' ) ]
resource.reindex()

resource.add_font('ShareTechMono-Regular.ttf')
share_tech_mono = font.load('Share Tech Mono')

resource.add_font('Cousine-Regular.ttf')
Cousine = font.load('Cousine')

resource.add_font('Cousine-Bold.ttf')
Cousine = font.load('Cousine', bold=True)

resource.add_font('Cousine-Italic.ttf')
Cousine = font.load('Cousine', italic=True)

resource.add_font('Cousine-BoldItalic.ttf')
Cousine = font.load('Cousine', bold=True, italic=True)

main_font = 'Cousine'

cubes = resource.image('cubes.png')
cubes_seq = pyglet.image.ImageGrid(cubes, 1, 9, item_width=CUBE_LENGTH)

cube_red = cubes_seq[0]
cube_orange = cubes_seq[1]
cube_yellow = cubes_seq[2]
cube_green = cubes_seq[3]
cube_skyblue = cubes_seq[4]
cube_blue = cubes_seq[5]
cube_purple = cubes_seq[6]
cube_grey = cubes_seq[7]
cube_ghost = cubes_seq[8]

pause = False
lines_count_draw = False
dev_mode = False
fps_draw = False
key_draw = False
current_figure_draw = False
current_orientation_draw = False

key_move_left = LEFT
key_move_right = RIGHT
key_rotate_clock = UP
key_rotate_cntrclock = Z
key_move_down = DOWN
key_hard_drop = SPACE
key_hold = LSHIFT
key_restart = RETURN
key_pause = BACKSPACE
key_dev = QUOTELEFT

start_interval = end_interval = 0
start_increase = end_increase = 0
increase_interval = 30
interval = 2


lines_cleared_label = pyglet.text.Label(
                          font_name=main_font,
                          font_size=14,
                          anchor_x='right', anchor_y='center')

lines_count_label = pyglet.text.Label(
                        font_name=main_font,
                        font_size=24, bold=True,
                        anchor_x='right', anchor_y='center')

time_elapsed_label = pyglet.text.Label(
                        font_name=main_font,
                        font_size=14,
                        anchor_x='right', anchor_y='center')

time_label = pyglet.text.Label(
                        font_name=main_font,
                        font_size=24, bold=True,
                        anchor_x='right', anchor_y='center')

hold_label = pyglet.text.Label(
                        font_name=main_font,
                        font_size=14,
                        anchor_x='right', anchor_y='center')

state_label = pyglet.text.Label(
                        font_name=main_font,
                        font_size=14,
                        anchor_x='center', anchor_y='center')

fps_label = pyglet.text.Label(anchor_x = 'left', anchor_y='top')
key_label = pyglet.text.Label(anchor_x = 'left', anchor_y='top')
current_figure_label = pyglet.text.Label(anchor_x = 'right', anchor_y='top')
current_orientation_label = pyglet.text.Label(anchor_x = 'right', anchor_y='top')

def generate_frame(width, height, screen_x, screen_y, batch=None):
    frame = []
    height += 2
    width += 2
    for x in range(width//2):
        for y in range(height):
            if (y == 0) | (x == width//2-1) & (not (y == height-1)):
                x_pos_left = (screen_x/2) - (CUBE_LENGTH * (x + 1))
                x_pos_right = (screen_x/2) + (CUBE_LENGTH * x)
                y_pos = (screen_y - CUBE_LENGTH*(height))/2 + CUBE_LENGTH * y + (CUBE_LENGTH*(1/2)*(1-(screen_y-WINDOW_MIN_Y)/(WINDOW_Y-WINDOW_MIN_Y)))
                frame.append(
                    pyglet.sprite.Sprite(img=cube_grey
                                        , x=x_pos_left
                                        , y=y_pos
                                        , batch=batch))
                frame.append(
                    pyglet.sprite.Sprite(img=cube_grey
                                        , x=x_pos_right
                                        , y=y_pos
                                        , batch=batch))
    return frame

cube_image = {
    'I': cube_skyblue, 
    'Z': cube_red, 
    'S': cube_green,
    'J': cube_blue,
    'L': cube_orange,
    'T': cube_purple,
    'O': cube_yellow
}

def generate_board(width, height, screen_x, screen_y, field, bound, figure, shadow, batch=None):
    board = []
    figure_coord = []
    shadow_coord = []
    full_height = height + bound
    for n in figure.matrix():
        figure_coord.append((figure.x + n % 4, full_height - 1 - (figure.y + n // 4)))
        shadow_coord.append((shadow.x + n % 4, full_height - 1 - (shadow.y + n // 4)))
    for row in range(full_height):
        for i in range(width):
            symbol = field[full_height - 1 - row][i]
            symbol_image = None
            if symbol == Game_Config.BLANK:
                if (i, row) in figure_coord:
                    symbol_image = cube_image[figure.type]
                elif (i, row) in shadow_coord:
                    symbol_image = cube_ghost
            else:
                symbol_image = cube_image[symbol]
            if symbol_image != None:
                y_pos = (screen_y - CUBE_LENGTH*(height))/2 + CUBE_LENGTH * row + (CUBE_LENGTH*(1/2)*(1-(screen_y-WINDOW_MIN_Y)/(WINDOW_Y-WINDOW_MIN_Y)))
                x_pos = (screen_x - CUBE_LENGTH*width)/2 + CUBE_LENGTH * i
                temp = pyglet.sprite.Sprite(img=symbol_image
                                        , x=x_pos
                                        , y=y_pos
                                        , batch=batch)
                if symbol_image == cube_ghost:
                    temp.opacity = 160
                board.append(temp)
    return board

def generate_hold(width, height, screen_x, screen_y, figure, exist, batch=None):
    hold = []
    if exist:
        for n in figure.matrix():
            row = (n//4 - figure.top_edge())
            col = figure.right_edge() - n%4
            x_pos = (screen_x - CUBE_LENGTH*width)/2 - CUBE_LENGTH * (2 + col) - 10
            y_pos = screen_y - (screen_y - CUBE_LENGTH*(height))/2 - CUBE_LENGTH * (3 + row)
            hold.append(
                    pyglet.sprite.Sprite(img=cube_image[figure.type]
                                        , x=x_pos
                                        , y=y_pos
                                        , batch=batch))
    return hold

key_state = key_state_old = set()

def key( k ):
    return k in key_state

def key_old( k ):
    return k in key_state_old


class GameScreen(pyglet.window.Window):

    def __init__(self, height, width):
        super().__init__(
            height
            , width
            , caption='PYTHON TETRIS GAME'
            , resizable=True)
        self.tetris = Tetris()
        self.line_count = self.tetris.lines_count
        self.time = 0
        self.max_time = 0
        self.batch = pyglet.graphics.Batch()
        self.dev_batch = pyglet.graphics.Batch()
        self.fps = 0
        self.set_minimum_size(WINDOW_MIN_X, WINDOW_MIN_Y)
        self.set_icon(cube_purple)
        self.game_frame = generate_frame(
            Game_Config.BOARD_WIDTH
            , Game_Config.BOARD_HEIGHT
            , self.width
            , self.height
            , self.batch
        )
        self.game_board = generate_board(
            Game_Config.BOARD_WIDTH
            , Game_Config.BOARD_HEIGHT
            , self.width
            , self.height
            , self.tetris.field
            , self.tetris.bound
            , self.tetris.figure
            , self.tetris.shadow
            , self.batch
        )
        self.game_hold = generate_hold(
            Game_Config.BOARD_WIDTH
            , Game_Config.BOARD_HEIGHT
            , self.width
            , self.height
            , self.tetris.hold_piece
            , self.tetris.is_hold()
            , self.batch
            )

    def on_draw(self):
        self.clear()
        self.game_frame = generate_frame(
            Game_Config.BOARD_WIDTH
            , Game_Config.BOARD_HEIGHT
            , self.width
            , self.height
            , self.batch)
        self.game_board = generate_board(
            Game_Config.BOARD_WIDTH
            , Game_Config.BOARD_HEIGHT
            , self.width
            , self.height
            , self.tetris.field
            , self.tetris.bound
            , self.tetris.figure
            , self.tetris.shadow
            , self.batch
        )
        self.game_hold = generate_hold(
            Game_Config.BOARD_WIDTH
            , Game_Config.BOARD_HEIGHT
            , self.width
            , self.height
            , self.tetris.hold_piece
            , self.tetris.is_hold()
            , self.batch
            )

        global lines_cleared_label
        lcl = lines_cleared_label
        lcl.text = 'LINES CLEARED'
        lcl.x=self.width/2 - ((Game_Config.BOARD_WIDTH+2)*CUBE_LENGTH)/2 - 10
        lcl.y=(self.height - (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 + (150*(self.height/WINDOW_Y))
        lcl.draw()

        global time_elapsed_label
        tel = time_elapsed_label
        tel.text = 'TIME ELAPSED'
        tel.x=self.width//2 - (6*CUBE_LENGTH) - 10
        tel.y=(self.height - (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 + (70*(self.height/WINDOW_Y))
        tel.draw()

        global hold_label
        hl = hold_label
        hl.text = 'HOLD'
        hl.x=self.width//2 - (6*CUBE_LENGTH) - 10
        hl.y=(self.height + (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 - (70*(self.height/WINDOW_Y))
        hl.draw()

        global lines_count_draw
        lcol = lines_count_label
        self.line_count = self.tetris.lines_count
        lcol.text = str(self.line_count)
        lcol.x=self.width//2 - (6*CUBE_LENGTH) - 10
        lcol.y=(self.height - (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 + (120*(self.height/WINDOW_Y))
        lcol.draw()

        global fps_draw, key_draw, current_figure_draw, current_orientation_draw

        fps_draw = key_draw = current_figure_draw = current_orientation_draw = dev_mode

        if current_figure_draw:
            cfl = current_figure_label
            cfl.text = f'{self.tetris.figure.type}'
            cfl.font_size = 20
            cfl.bold = True
            cfl.x, cfl.y = self.width-10, self.height-5
            cfl.batch = self.dev_batch

        if current_orientation_draw:
            col = current_orientation_label
            col.text = f'{self.tetris.figure.matrix()}'
            col.font_size = 20
            col.bold = True
            col.x, col.y = self.width-10, self.height-30
            col.batch = self.dev_batch

        if fps_draw:
            fl = fps_label
            fl.text = f'{self.fps:.1f} FPS'
            fl.font_size = 10
            fl.x, fl.y = 5, self.height-5
            fl.batch = self.dev_batch

        if key_draw:
            kl = key_label
            if len(key_state) > 0:
                kl.text = f'Key: {keyboard_input.keys[next(iter(key_state))]}'
            else:
                kl.text = f'Key:'
            kl.font_size = 10
            kl.x, kl.y = 5, self.height-20
            kl.batch = self.dev_batch

        if dev_mode:
            self.dev_batch.draw()

        self.batch.draw()

        if self.tetris.state == 'gameover':
            sl = state_label
            sl.text = 'GAME OVER'
            sl.x = self.width//2
            sl.y = self.height//2
            sl.draw()
        else:
            if self.tetris.state == 'start':
                self.max_time = self.time
            global pause
            if pause:
                sl = state_label
                sl.text = 'PAUSE'
                sl.x = self.width//2
                sl.y = self.height//2
                sl.draw()
        tl = time_label
        tl.x=self.width//2 - (6*CUBE_LENGTH) - 10
        tl.y=(self.height - (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 + (40*(self.height/WINDOW_Y))
        hr = int(self.max_time // 3600)
        min = int((self.max_time % 3600) // 60)
        sec = int((self.max_time % 3600) % 60)
        tl.text = f'{hr:02}:{min:02}:{sec:02}'
        tl.batch = self.batch

    def update(self, dt):
        global pause
        if pause == False:
            self.time += dt
        self.fps = 1/dt

    def on_key_press(self, symbol, modifiers):
        key_state.add( symbol )
    
    def on_key_release(self, symbol, modifiers):
        key_state.discard( symbol )

    def restart(self):
        global pause, increase_interval, interval
        pause = False
        self.tetris = Tetris()
        self.time = self.max_time = 0
        self.line_count = self.tetris.lines_count
        increase_interval = 30
        interval = 2



def move_objects(dt, screen):

    global dev_mode, key_dev, key_state, key_state_old, pause, key_move_left, key_move_right, key_rotate_clock, key_rotate_cntrclock, key_move_down, key_hard_drop, key_restart
    global start_interval, end_interval, interval, start_increase, end_increase

    if key ( key_dev ) and not key_old( key_dev ):
        dev_mode = not dev_mode

    if key( key_pause ) and not key_old( key_pause ):
        pause = not pause

    end_interval = end_increase = screen.time

    if screen.tetris.state == 'start' and not pause:

        global increase_interval

        if key( key_move_down ) and not key_old( key_move_down ):
            screen.tetris.descend()
            start_interval += interval*0.05

        if key( key_hard_drop ) and not key_old( key_hard_drop ):
            screen.tetris.hard_drop()
            
        if key( key_hold ) and not key_old( key_hold ):
            screen.tetris.hold()
            
        if key( key_move_left ) and not key_old( key_move_left ):
            screen.tetris.move(-1)

        if key( key_move_right ) and not key_old( key_move_right ):
            screen.tetris.move(1)
        
        if key( key_rotate_clock ) and not key_old( key_rotate_clock ):
            screen.tetris.rotate('clock')
            start_interval += interval*0.05

        if key( key_rotate_cntrclock ) and not key_old( key_rotate_cntrclock ):
            screen.tetris.rotate('counter')
            start_interval += interval*0.05

        if end_increase-start_increase >= increase_interval:
            interval *= 0.92
            increase_interval *= 0.90
            start_increase = end_increase
            
        if (end_interval-start_interval >= interval) and not (key( key_move_down ) or key( key_hard_drop )):
            # print(f"{end_interval-start_interval:.2f} - descend piece")
            screen.tetris.descend()
            start_interval = end_interval
    else:
        if key( key_restart ) and not key_old( key_restart ):
            screen.restart()
            start_interval = start_increase = screen.time

    key_state_old = key_state.copy()

def run():
    screen = GameScreen(WINDOW_Y, WINDOW_X)
    pyglet.clock.schedule_interval(screen.update, 1/60)
    pyglet.clock.schedule(move_objects, screen)
    pyglet.app.run()

