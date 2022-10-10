import pyglet
from pyglet import image
import random

'''
class Figure():
    def __init__(self):
        # self.rot = 
        # self.type =
'''

window = pyglet.window.Window(900
                              ,700
                              ,caption='PYTHON TETRIS GAME'
                              # ,resizable=True
                              )

pic = image.load('ref/1200px-Typical_Tetris_Game.svg.png')
pic.anchor_x = pic.width // 2
pic.anchor_y = pic.height // 2
picSprite = pyglet.sprite.Sprite(pic)
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
    label.draw()
    


pyglet.app.run()