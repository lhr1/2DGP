import random

from pico2d import *

class BackGround:
    day_img = None
    change_img = []
    night_img = None
    def __init__(self):
        if BackGround.day_img == None:
            BackGround.day_img = load_image('resource/BG/BG_day3.png')
            BackGround.change_img.append(load_image('resource/BG/BG_change0.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change1.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change2.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change3.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change4.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change5.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change6.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change7.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change8.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change9.png'))
            BackGround.change_img.append(load_image('resource/BG/BG_change10.png'))
        if BackGround.night_img == None:
            BackGround.night_img = load_image('resource/BG/BG_night.png')

    def draw(self, pos_line):
        if pos_line <= 30:
            BackGround.day_img.draw(400, 300)
        elif 30 < pos_line and pos_line <= 41:
            BackGround.change_img[pos_line - 31].draw(400, 300)
        elif pos_line > 41:
            BackGround.night_img.draw(400, 300)