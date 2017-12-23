import game_framework
import main_state
from pico2d import *


name = "GameOverState"
image = None
running = True
GameOverImg = None
SpaceImg = None


class GameOver:
    image = []
    BG_0, BG_1, BG_2, Over, Space = 0, 1, 2, 3, 3
    state = BG_0

    def __init__(self):
        GameOver.image.append(load_image('resource/GAMEOVER/BG_night.png'))
        GameOver.image.append(load_image('resource/GAMEOVER/BG_night1.png'))
        GameOver.image.append(load_image('resource/GAMEOVER/BG_night2.png'))
        GameOver.image.append(load_image('resource/GAMEOVER/GameOver.png'))
        self.bgm = load_music('resource/bgm/[BT21] Meet TATA.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def draw(self):
        if GameOver.image != None:
            GameOver.image[GameOver.state].draw(400, 300, 800, 600)

    def update(self):
        if GameOver.image != None:
            if GameOver.state < GameOver.Over:
                GameOver.state += 1
                if GameOver.state == 3:
                    GameOver.state = GameOver.Over
                delay(0.1)
            elif GameOver.state == GameOver.Over:
                GameOver.state = GameOver.Space


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
    global GameOverImg, SpaceImg
    GameOver.state = GameOver.BG_0
    GameOverImg = GameOver()
    SpaceImg = CSpace()


def exit():
    global GameOverImg, SpaceImg
    del(GameOverImg)
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
    GameOverImg.draw()
    if GameOver.state == GameOver.Space:
        SpaceImg.draw()
    update_canvas()


def update():
    if not running:
        game_framework.quit()   #quit은 exit를 호출한다. 앞 상태의 resume을 수행한다.

    GameOverImg.update()


def pause():
    pass


def resume():
    pass






