import pyglet
from pyglet import image
import random
import os

        

# Constants
#------------------------------------------

WINDOW_X = 900
WINDOW_Y = 740
CUBE_LENGTH = 30

#------------------------------------------

window = pyglet.window.Window(WINDOW_X
                              ,WINDOW_Y
                              ,caption='PYTHON TETRIS GAME'
                              # ,resizable=True
                              )


cubes = image.load('resources/img/cubes.png')
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
    def __init__(self, type, x=(WINDOW_X/2), y=((WINDOW_Y-22*CUBE_LENGTH)/2 + CUBE_LENGTH), rot=0):
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

gameFrame = generateFrame(22, frameBatch)

#------------------------------------------

temp = pyglet.graphics.Batch()

thing1 = pyglet.sprite.Sprite(img=cubeRed, x=WINDOW_X/2, y=WINDOW_Y/2, batch=temp)

pic = image.load('ref/1200px-Typical_Tetris_Game.svg.png')
pic.anchor_x = pic.width // 2
pic.anchor_y = pic.height // 2
picSprite = pyglet.sprite.Sprite(pic)
picSprite.opacity = 50
picSprite.scale = 700 / 2200
picSprite.position = (window.width//2, window.height//2)

label = pyglet.text.Label('Score',
                          font_name='Times New Roman',
                          font_size=20,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    picSprite.draw()
    frameBatch.draw()
    temp.draw()
    label.draw()


pyglet.app.run()