import pyglet
from pyglet import image
import random
import os

'''
class Figure():
    def __init__(self):
        # self.rot = 
        # self.type =
'''

# Constants
#------------------------------------------

WINDOW_X = 900
WINDOW_Y = 700
CUBE_LENGTH = 32

#------------------------------------------

window = pyglet.window.Window(WINDOW_X
                              ,WINDOW_Y
                              ,caption='PYTHON TETRIS GAME'
                              # ,resizable=True
                              )



cubes = image.load('resources/img/cubes.png')
cubesSeq = pyglet.image.ImageGrid(cubes, 1, 7)

cubeRed = cubesSeq[0]
cubeOrange = cubesSeq[1]
cubeYellow = cubesSeq[2]
cubeGreen = cubesSeq[3]
cubeBlue = cubesSeq[4]
cubePurple = cubesSeq[5]
cubeGrey = cubesSeq[6]


# Create the grey frame outline for game

frameBatch = pyglet.graphics.Batch()

def generateFrame(height, batch=None):
    frame = []
    for x in range(6):
        for y in range(height):
            if (y == 0) | (x == 5) | (y == height-1):
                xPosLeft = (WINDOW_X//2) - (CUBE_LENGTH * (x + 1))
                xPosRight = (WINDOW_X//2) + (CUBE_LENGTH * x)
                yPos = CUBE_LENGTH * y
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
    label.draw()


pyglet.app.run()