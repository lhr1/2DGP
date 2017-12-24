import game_framework
import start_state
from pico2d import *


name = "GameClearState"
image = None
running = True
GameClearImg = None
SpaceImg = None


class GameClear:
    image = []
    BG_0, BG_1, BG_2, BG_3, BG_4, Clear, Space = 0, 1, 2, 3, 4, 5, 5
    state = BG_0

    def __init__(self):
        GameClear.image.append(load_image('resource/GAMECLEAR/BG_clear0.png'))
        GameClear.image.append(load_image('resource/GAMECLEAR/BG_clear1.png'))
        GameClear.image.append(load_image('resource/GAMECLEAR/BG_clear2.png'))
        GameClear.image.append(load_image('resource/GAMECLEAR/BG_clear3.png'))
        GameClear.image.append(load_image('resource/GAMECLEAR/BG_clear4.png'))
        #GameClear.image.append(load_image('resource/GAMECLEAR/BG_clear5.png'))
        GameClear.image.append(load_image('resource/GAMECLEAR/BG_clear6.png'))

        self.bgm = load_music('resource/bgm/gameclear.mp3')
        self.bgm.set_volume(64)
        self.bgm.play()

    def draw(self):
        if GameClear.image != None:
            GameClear.image[GameClear.state].draw(400, 300, 800, 600)

    def update(self):
        if GameClear.image != None:
            if GameClear.state < GameClear.Clear:
                GameClear.state += 1
                if GameClear.state == 5:
                    GameClear.state = GameClear.Clear
                delay(0.2)
            elif GameClear.state == GameClear.Clear:
                GameClear.state = GameClear.Space


class CSpace:
    def __init__(self):
        self.image = load_image('resource/title_SPACE.png')
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
    global GameClearImg, SpaceImg
    GameClear.state = GameClear.BG_0
    GameClearImg = GameClear()
    SpaceImg = CSpace()


def exit():
    global GameClearImg, SpaceImg
    del(GameClearImg)
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
                game_framework.change_state(start_state)


def draw():
    clear_canvas()
    GameClearImg.draw()
    if GameClear.state == GameClear.Space:
        SpaceImg.draw()
    update_canvas()


def update():
    if not running:
        game_framework.quit()   #quit은 exit를 호출한다. 앞 상태의 resume을 수행한다.

    GameClearImg.update()


def pause():
    pass


def resume():
    pass






