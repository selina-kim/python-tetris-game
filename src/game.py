import pyglet
from pyglet.window.key import *
from pyglet import resource
from pyglet import font

import os
from tetris_engine import Game_Config
from tetris_engine import Tetris

# Constants ----------------------
WINDOW_X = 900
WINDOW_Y = 740
WINDOW_MIN_Y = 630
WINDOW_MIN_X = 360
CUBE_LENGTH = 30
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
cubes_seq = pyglet.image.ImageGrid(cubes, 1, 8)

cube_red = cubes_seq[0]
cube_orange = cubes_seq[1]
cube_yellow = cubes_seq[2]
cube_green = cubes_seq[3]
cube_skyblue = cubes_seq[4]
cube_blue = cubes_seq[5]
cube_purple = cubes_seq[6]
cube_grey = cubes_seq[7]

pause = False
lines_count_draw = False
fps_draw = True
resize = False

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

state_label = pyglet.text.Label(
                        font_name=main_font,
                        font_size=14,
                        anchor_x='center', anchor_y='center')

fps_label = pyglet.text.Label(anchor_x = 'left', anchor_y='top')

def generate_frame(width, height, screen_x, screen_y, batch=None):
    frame = []
    height += 2
    width += 2
    for x in range(6):
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

key_state = key_state_old = set()

def key( k ):
    return k in key_state

def key_old( k ):
    return k in key_state_old


class GameScreen(pyglet.window.Window):

    tetris = Tetris()

    def __init__(self, height, width):
        super().__init__(
            height
            , width
            , caption='PYTHON TETRIS GAME'
            , resizable=True)
        self.line_count = 0
        self.time = 0
        self.max_time = 0
        self.batch = pyglet.graphics.Batch()
        self.fps = 0
        self.set_minimum_size(WINDOW_MIN_X, WINDOW_MIN_Y)
        self.set_icon(cube_purple)
        self.game_frame = generate_frame(
            Game_Config.BOARD_WIDTH
            , Game_Config.BOARD_HEIGHT
            , self.width
            , self.height
            , self.batch)

    def on_draw(self):
        self.clear()
        self.game_frame = generate_frame(
            Game_Config.BOARD_WIDTH
            , Game_Config.BOARD_HEIGHT
            , self.width
            , self.height
            , self.batch)

        global lines_cleared_label
        lcl = lines_cleared_label
        lcl.text = 'LINES CLEARED'
        lcl.x=self.width/2 - ((Game_Config.BOARD_WIDTH+2)*CUBE_LENGTH)/2 - 10
        lcl.y=(self.height - (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 + (150*(self.height/WINDOW_Y))  #(Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH - 480
        lcl.batch = self.batch

        global time_elapsed_label
        tel = time_elapsed_label
        tel.text = 'TIME ELAPSED'
        tel.x=self.width//2 - (6*CUBE_LENGTH) - 10
        tel.y=(self.height - (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 + (70*(self.height/WINDOW_Y))
        tel.batch = self.batch

        global lines_count_draw
        lcol = lines_count_label
        if lines_count_draw:
            self.line_count = self.tetris.lines_count
            lines_count_draw = False
        lcol.text = str(self.line_count)
        lcol.x=self.width//2 - (6*CUBE_LENGTH) - 10
        lcol.y=(self.height - (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 + (120*(self.height/WINDOW_Y))
        lcol.batch = self.batch

        if self.tetris.state == 'start':
            self.max_time = self.time
        else:
            sl = state_label
            sl.text = 'GAME OVER'
            sl.x = self.width//2
            sl.y = self.height//2
            sl.batch = self.batch

        global pause
        if pause:
            sl = state_label
            sl.text = 'PAUSE'
            sl.x = self.width//2
            sl.y = self.height//2
            sl.batch = self.batch
        tl = time_label
        tl.x=self.width//2 - (6*CUBE_LENGTH) - 10
        tl.y=(self.height - (Game_Config.BOARD_HEIGHT+2)*CUBE_LENGTH)/2 + (40*(self.height/WINDOW_Y))
        hr = int(self.max_time // 3600)
        min = int((self.max_time % 3600) // 60)
        sec = int((self.max_time % 3600) % 60)
        tl.text = f'{hr:02}:{min:02}:{sec:02}'
        tl.batch = self.batch

        if fps_draw:
            fl = fps_label
            fl.text = f'{self.fps:.1f} FPS'
            fl.font_size = 10
            fl.x, fl.y = 5, self.height-5
            fl.batch = self.batch

        self.batch.draw()

    def update(self, dt):
        global pause
        if pause == False:
            self.time += dt
        self.fps = 1/dt

    def on_key_press(self, symbol, modifiers):
        key_state.add( symbol )
    
    def on_key_release(self, symbol, modifiers):
        key_state.discard( symbol )


def move_objects(dt, screen):

    global key_state, key_state_old, pause

    if key( ESCAPE ) and not key_old( ESCAPE ):
        pause = not pause

    if key( LEFT ) and not key_old( LEFT ):
        print("pressed left")
        screen.tetris.move(-1)

    if key( RIGHT ) and not key_old( RIGHT ):
        print("pressed right")
        screen.tetris.move(1)

    if key( UP ) and not key_old( UP ):
        print("pressed up")
        screen.tetris.rotate('clock')

    if key( DOWN ) and not key_old( DOWN ):
        print("pressed down")
        screen.tetris.descend()

    if key( SPACE ) and not key_old( SPACE ):
        print("pressed space bar")
        screen.tetris.hard_drop()
    
    if screen.tetris.is_freeze:
        global lines_count_draw
        lines_count_draw = True

    key_state_old = key_state.copy()

def run(h, w):
    screen = GameScreen(h, w)
    pyglet.clock.schedule_interval(screen.update, 1/60)
    pyglet.clock.schedule(move_objects, screen)
    pyglet.app.run()

