import pyglet
from pyglet import resource
from pyglet import font
import random
import os

#------------------------------------------

resource.path = ['../data']
resource.reindex()

resource.add_font('font/RedHatDisplay-Regular.ttf')
redHat = font.load('Red Hat Display')

resource.add_font('font/RedHatDisplay-Bold.ttf')
redHatBold = font.load('Red Hat Display', bold=True)


# Constants
#------------------------------------------

WINDOW_X = 900
WINDOW_Y = 740
BOARD_HEIGHT = 22 # in terms of num of cubes
CUBE_LENGTH = 30

#------------------------------------------

window = pyglet.window.Window(WINDOW_X
                              ,WINDOW_Y
                              ,caption='PYTHON TETRIS GAME'
                              # ,resizable=True
                              )


cubes = resource.image('img/cubes.png')
cubesSeq = pyglet.image.ImageGrid(cubes, 1, 8)

cubeRed = cubesSeq[0]
cubeOrange = cubesSeq[1]
cubeYellow = cubesSeq[2]
cubeGreen = cubesSeq[3]
cubeSkyblue = cubesSeq[4]
cubeBlue = cubesSeq[5]
cubePurple = cubesSeq[6]
cubeGrey = cubesSeq[7]

class Figure():
    def __init__(self, type, x=(WINDOW_X/2), y=((WINDOW_Y-BOARD_HEIGHT*CUBE_LENGTH)/2 + CUBE_LENGTH), rot=0):
        self.x = x
        self.y = y
        self.type = type
        self.rot = rot
    

# Create the grey frame outline for game

frameBatch = pyglet.graphics.Batch()

def generateFrame(height, batch=None):
    frame = []
    for x in range(6):
        for y in range(height):
            if (y == 0) | (x == 5) & (not (y == height-1)):
                xPosLeft = (WINDOW_X/2) - (CUBE_LENGTH * (x + 1))
                xPosRight = (WINDOW_X/2) + (CUBE_LENGTH * x)
                yPos = (WINDOW_Y - CUBE_LENGTH*height)/2 + CUBE_LENGTH * y
                # print("block at x=" + str(xPosLeft) + ", y=" + str(yPos) + " and x=" + str(xPosRight) + ", y=" + str(yPos))
                frame.append(
                    pyglet.sprite.Sprite(img=cubeGrey
                                        , x=xPosLeft
                                        , y=yPos
                                        , batch=batch))
                frame.append(
                    pyglet.sprite.Sprite(img=cubeGrey
                                        , x=xPosRight
                                        , y=yPos
                                        , batch=batch))
    return frame

gameFrame = generateFrame(BOARD_HEIGHT, frameBatch)

#------------------------------------------

temp = pyglet.graphics.Batch()

thing1 = pyglet.sprite.Sprite(img=cubeRed, x=WINDOW_X/2, y=WINDOW_Y/2, batch=temp)

pic = resource.image('ref/1200px-Typical_Tetris_Game.svg.png')
pic.anchor_x = pic.width // 2
pic.anchor_y = pic.height // 2
picSprite = pyglet.sprite.Sprite(pic)
picSprite.opacity = 50
picSprite.scale = 700 / 2200
picSprite.position = (window.width//2, window.height//2, 0)

textLinesCount = pyglet.text.Label('LINES CLEARED',
                          font_name='Red Hat Display',
                          font_size=16,
                          x=window.width//2 - (6*CUBE_LENGTH) - 10, y=BOARD_HEIGHT*CUBE_LENGTH,
                          anchor_x='right', anchor_y='center')

textTimeCount = pyglet.text.Label('TIME ELAPSED',
                          font_name='Red Hat Display',
                          font_size=16,
                          x=window.width//2 - (6*CUBE_LENGTH) - 10, y=BOARD_HEIGHT*CUBE_LENGTH - 100,
                          anchor_x='right', anchor_y='center')
                        

@window.event
def on_draw():
    window.clear()
    # picSprite.draw()
    frameBatch.draw()
    temp.draw()
    textLinesCount.draw()
    textTimeCount.draw()


pyglet.app.run()