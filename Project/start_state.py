import game_framework
import title_state
from pico2d import *


name = "StartState"
image = None
logo_time = 0.0
start_bgm = None


def enter():
    global image, start_bgm
    image = load_image('resource/start_img.png')
    start_bgm = load_music('resource/bgm/[BT21] Meet TATA.mp3')
    start_bgm.set_volume(64)
    start_bgm.repeat_play()


def exit():
    global image
    del(image)


def update():
    global logo_time

    if(logo_time > 1.8):
        logo_time = 0
        game_framework.change_state(title_state)
    delay(0.01)
    logo_time += 0.01


def draw():
    global imgae
    clear_canvas()
    image.draw(400, 300)
    update_canvas()



def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass




