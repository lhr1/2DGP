import game_framework
import main_state
from pico2d import *


name = "TitleState"
image = None
running = True
SpaceImg = None

class CSpace:
    def __init__(self):
        self.image= load_image('resource/title_SPACE.png')
        self.x, self.y = 400, 150
        self.show = True
    def draw(self):
        if self.show == True:
            self.image.draw(self.x, self.y)
            delay(0.2)
            self.show = False
        elif self.show == False:
            delay(0.5)
            self.show = True


def enter():
    global image
    global SpaceImg
    image = load_image('resource/title.png')
    SpaceImg = CSpace()


def exit():
    global image
    global SpaceImg
    del(image)
    del(SpaceImg)



def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                running = False
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    clear_canvas()
    image.draw(400, 300)
    SpaceImg.draw()
    update_canvas()


def update():
    if not running:
        game_framework.quit()   #quit은 exit를 호출한다. 앞 상태의 resume을 수행한다.


def pause():
    pass


def resume():
    pass






