import random

from pico2d import *

class BackGround:
    def __init__(self):
        self.image = load_image('resource/BG_day.png')

    def draw(self):
        self.image.draw(400, 300)