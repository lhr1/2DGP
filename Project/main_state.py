import random
import json
import os
from pico2d import *

import game_framework
import title_state
import game_clear
import game_over
from BackGround import BackGround
from Position import Position


name = "MainState"

background = None
bb_show = False
main_bgm = None
#chimmy
chimmy = None
chimmy_dead = False
clear  = False
#dragon
dragon = None
#map
map_data = None
stage1 = None
position = None
#monster
monster_team = []
monster = None
#firewall
firewall_team = []



class Map:
    global map_data, map_next_data, stage1, stage_next, position, monster_team
    imgSTONE, imgWALL, imgHINDRANCE, imgEMPTY, imgCLEAR = None, None, None, None, None
    STONE, WALL, HINDRANCE, MONSTER_K, MONSTER_T, EMPTY, CLEAR, FIREWALL = 0, 1, 2, 3, 4, 5, 6, 7
    LINEMAX = 7
    ROWMAX = 110

    rowcnt = 0
    MAPSIZE = (LINEMAX - 1) * (ROWMAX - 1)
    MapPos = 0
    BLOCKSIZE = 70
    DownCnt = 0

    def __init__(self):
        if Map.imgSTONE == None:
            Map.imgSTONE = load_image('resource/stone2.png')
        if Map.imgWALL == None:
            Map.imgWALL = load_image('resource/wall3.png')
        if Map.imgHINDRANCE == None:
            Map.imgHINDRANCE = load_image('resource/hindrance.png')
        if Map.imgEMPTY == None:
            Map.imgEMPTY = load_image('resource/empty2.png')
        if Map.imgCLEAR == None:
            Map.imgCLEAR = load_image('resource/clear_tile.png')
        self.row = []
        self.state = []
        self.randnum = []

    def draw(self):
        # 타일 타입 맞춰서 그림 그리기
        #STONE, WALL, HINDRANCE, MONSTER, EMPTY
            for row in range(Map.ROWMAX):
                for line in range(Map.LINEMAX):
                    self.MapPos = row * (Map.LINEMAX) + line
                    if map_data[row].state[line] == Map.STONE:
                        self.imgSTONE.clip_draw(map_data[row].randnum[line]*80, 0, Map.BLOCKSIZE, Map.BLOCKSIZE, position[self.MapPos].x, position[self.MapPos].y + Map.DownCnt)
                    elif map_data[row].state[line] == Map.WALL:
                        self.imgWALL.clip_draw(map_data[row].randnum[line]*80, 0, Map.BLOCKSIZE, Map.BLOCKSIZE, position[self.MapPos].x, position[self.MapPos].y + Map.DownCnt)
                    elif map_data[row].state[line] == Map.HINDRANCE:
                        self.imgEMPTY.clip_draw(map_data[row].randnum[line] * 80, 0, Map.BLOCKSIZE, Map.BLOCKSIZE,
                                                position[self.MapPos].x, position[self.MapPos].y + Map.DownCnt)
                        self.imgHINDRANCE.clip_draw(0, 0, Map.BLOCKSIZE, Map.BLOCKSIZE, position[self.MapPos].x, position[self.MapPos].y + Map.DownCnt)
                    elif map_data[row].state[line] == Map.MONSTER_K or map_data[row].state[line] == Map.MONSTER_T or map_data[row].state[line] == Map.EMPTY:
                        map_data[row].state[line] = Map.EMPTY
                        self.imgEMPTY.clip_draw(map_data[row].randnum[line]*80, 0, Map.BLOCKSIZE, Map.BLOCKSIZE, position[self.MapPos].x, position[self.MapPos].y+ Map.DownCnt)
                    elif map_data[row].state[line] == Map.CLEAR:
                        self.imgCLEAR.clip_draw(0, 0, Map.BLOCKSIZE, Map.BLOCKSIZE, position[self.MapPos].x, position[self.MapPos].y + Map.DownCnt)


    def update(self):
        pass


class Monster:
    global map_data, monster_team, position
    imgMONSTER_K, imgMONSTER_T = None, None
    mon_num = 0
    speed = 1
    die_sound = None

    def __init__(self):
        if Monster.imgMONSTER_K == None:
            Monster.imgMONSTER_K = load_image('resource/monster_suki.png')
        if Monster.imgMONSTER_T == None:
            Monster.imgMONSTER_T = load_image('resource/monster_tata.png')
        if Monster.die_sound == None:
            Monster.die_sound = load_wav('resource/bgm/monsterdie.wav')
            Monster.die_sound.set_volume(64)

        self.x = 0
        self.y = 0
        self.type = Map.MONSTER_K
        self.frame_cnt = 0
        self.frame = random.randint(0, 3)
        self.dir = random.randint(0, 1)
        self.pos_row = 0
        self.pos_line = 0
        self.movecnt = 0

    cnt_max_t = 40
    cnt_max_k = 10

    def draw_k(self):
        for num in range(Monster.mon_num):
            if monster_team[num].type == Map.MONSTER_K:
                monster_team[num].frame_cnt = (monster_team[num].frame_cnt + 1) % Monster.cnt_max_k
                if monster_team[num].frame_cnt == 0:
                    monster_team[num].frame = (monster_team[num].frame + 1) % 4
                monster_team[num].imgMONSTER_K.clip_draw(monster_team[num].frame * Map.BLOCKSIZE
                                                         , monster_team[num].dir * Map.BLOCKSIZE
                                                         , Map.BLOCKSIZE, Map.BLOCKSIZE, monster_team[num].x, monster_team[num].y + Map.DownCnt)

    def draw_t(self):
        for num in range(Monster.mon_num):
            if monster_team[num].type == Map.MONSTER_T:
                monster_team[num].frame_cnt = (monster_team[num].frame_cnt + 1) % Monster.cnt_max_t
                if monster_team[num].frame_cnt == 0:
                    monster_team[num].frame = (monster_team[num].frame + 1) % 4
                monster_team[num].imgMONSTER_T.clip_draw(monster_team[num].frame * Map.BLOCKSIZE
                                                         , monster_team[num].dir * Map.BLOCKSIZE
                                                         , Map.BLOCKSIZE, Map.BLOCKSIZE, monster_team[num].x, monster_team[num].y + Map.DownCnt)

    def update_k(self):
        for num in range(Monster.mon_num):
            if monster_team[num].type == Map.MONSTER_K:
                self.move(num)

    def update_t(self):
        for num in range(Monster.mon_num):
            if monster_team[num].type == Map.MONSTER_T \
                    and monster_team[num].pos_row == Chimmy.pos_line:
                self.move(num)

    def move(self, num):
        if monster_team[num].dir == 0:       #right
            if map_data[monster_team[num].pos_row].state[monster_team[num].pos_line + 1] ==  Map.EMPTY:
                if map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line + 1] == Map.WALL \
                    or map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line + 1] == Map.STONE:
                    monster_team[num].x = min(position[monster_team[num].pos_line + 1].x, monster_team[num].x + Monster.speed)
                    monster_team[num].movecnt = monster_team[num].movecnt + Monster.speed
                    if monster_team[num].movecnt == Map.BLOCKSIZE:
                        monster_team[num].pos_line += 1
                        monster_team[num].movecnt = 0
                elif map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line + 1] == Map.EMPTY\
                        and map_data[monster_team[num].pos_row].state[monster_team[num].pos_line - 1] != Map.EMPTY:
                    monster_team[num].dir = 0
                else:
                    monster_team[num].dir = 1
                    monster_team[num].movecnt = 0
            else:
                monster_team[num].dir = 1
                monster_team[num].movecnt = 0
                if map_data[monster_team[num].pos_row].state[monster_team[num].pos_line - 1] !=  Map.EMPTY:
                    monster_team[num].dir = 0
        elif monster_team[num].dir == 1:       #left
            if map_data[monster_team[num].pos_row].state[monster_team[num].pos_line - 1] == Map.EMPTY:
                if map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line - 1] == Map.WALL \
                    or map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line - 1] ==  Map.STONE:
                    monster_team[num].x = max(position[monster_team[num].pos_line - 1].x, monster_team[num].x - Monster.speed)
                    monster_team[num].movecnt = monster_team[num].movecnt + Monster.speed
                    if monster_team[num].movecnt == Map.BLOCKSIZE:
                        monster_team[num].pos_line -= 1
                        monster_team[num].movecnt = 0
                elif map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line - 1] == Map.EMPTY \
                        and map_data[monster_team[num].pos_row].state[monster_team[num].pos_line + 1] != Map.EMPTY:
                    monster_team[num].dir = 1
                else:
                    monster_team[num].dir = 0
                    monster_team[num].movecnt = 0
            else:
                monster_team[num].dir = 0
                monster_team[num].movecnt = 0
                if map_data[monster_team[num].pos_row].state[monster_team[num].pos_line + 1] !=  Map.EMPTY:
                    monster_team[num].dir = 1

    def get_bb(self):
        return self.x - (Map.BLOCKSIZE / 3), self.y - (Map.BLOCKSIZE / 2) + Map.DownCnt\
            , self.x + (Map.BLOCKSIZE / 3), self.y + (Map.BLOCKSIZE / 2) + Map.DownCnt

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def die(self):
        self.die_sound.play()


class FireWall:
    global map_data, firewall_team, position
    imgFIREWALL, imgFIRE = None, None
    firewall_num = 0
    SPEED = 4
    FIRE_SIZE = 60

    def __init__(self):
        if FireWall.imgFIREWALL == None:
            FireWall.imgFIREWALL = load_image('resource/firetile2.png')
        if FireWall.imgFIRE == None:
            FireWall.imgFIRE = load_image('resource/firetile_fire.png')
        self.x, self.y = 0, 0
        self.fire_x, self.fire_y = self.x, self.y
        self.pos_row, self.pos_line = 0, 0
        self.fire_cnt = 0
        self.fire_speed = random.randint(1, 10)
        self.fire_show = False

    def draw(self):
        for num in range(FireWall.firewall_num):
            firewall_team[num].imgFIREWALL.draw(firewall_team[num].x
                                                , firewall_team[num].y + Map.DownCnt
                                                , Map.BLOCKSIZE, Map.BLOCKSIZE)
            if firewall_team[num].fire_cnt == 0:
                firewall_team[num].fire_x = firewall_team[num].x - (Map.BLOCKSIZE / 2)
                firewall_team[num].fire_show = False
            elif 200 < firewall_team[num].fire_cnt:
                firewall_team[num].fire_show = True
            firewall_team[num].fire_cnt += firewall_team[num].fire_speed
            if firewall_team[num].fire_show == True:
                firewall_team[num].fire_x -= firewall_team[num].SPEED
                if firewall_team[num].fire_x <= position[1].x:
                    firewall_team[num].fire_cnt = 0
                firewall_team[num].fire_y = firewall_team[num].y + Map.DownCnt
                firewall_team[num].imgFIRE.draw(firewall_team[num].fire_x
                                            , firewall_team[num].fire_y
                                            , FireWall.FIRE_SIZE, FireWall.FIRE_SIZE - 10)


    def update(self):
        for num in range(FireWall.firewall_num):
            pass


    def get_bb(self):
        #return self.x - (Map.BLOCKSIZE / 2), self.y - (Map.BLOCKSIZE / 2)\
        #     , self.x + (Map.BLOCKSIZE / 2), self.y + (Map.BLOCKSIZE / 2)
        return self.fire_x - (FireWall.FIRE_SIZE / 2), self.fire_y - (FireWall.FIRE_SIZE / 3) \
            , self.fire_x + (FireWall.FIRE_SIZE / 2), self.fire_y + (FireWall.FIRE_SIZE / 3)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Dragon:
    image = []
    fire_img = None
    ATK, FLY, SLEEP_DOWN, SLEEP_UP, WAKEUP = 0, 1, 2, 3, 4
    state = SLEEP_DOWN
    M_SLEEP, M_LEFT, M_RIGHT, M_UP, M_DOWN = 0, 1, 2, 3, 4
    move_state = M_SLEEP
    pos_row = 3
    pos_line = 4
    movecnt = 0
    staycnt = 0
    SPEED = 2
    atk_stop = False

    atk_sound = None

    def __init__(self):
        Dragon.image.append(load_image('resource/DRAGON/dragon_atk.png'))
        Dragon.image.append(load_image('resource/DRAGON/dragon_fly.png'))
        Dragon.image.append(load_image('resource/DRAGON/dragon_sleep_down.png'))
        Dragon.image.append(load_image('resource/DRAGON/dragon_sleep_up.png'))
        Dragon.image.append(load_image('resource/DRAGON/dragon_wakeup.png'))
        if Dragon.fire_img == None:
            Dragon.fire_img = load_image('resource/DRAGON/dragon_fire.png')
        Dragon.pos_row = 3
        Dragon.pos_line = 2
        Dragon.state = Dragon.SLEEP_DOWN
        Dragon.move_state = Dragon.M_SLEEP
        Dragon.movecnt = 0
        Dragon.staycnt = 0
        self.x, self.y = position[Dragon.pos_line * (Map.LINEMAX) + Dragon.pos_row].x\
            , position[Dragon.pos_line * (Map.LINEMAX) + Dragon.pos_row].y + Map.BLOCKSIZE / 2
        self.size_x, self.size_y = 350, 180
        self.fire_x, self.fire_y = position[0].x, self.y
        self.size_fire_x, self.size_fire_y = 0, Map.BLOCKSIZE
        atk_stop = False

        if Dragon.atk_sound == None:
            Dragon.atk_sound = load_wav('resource/bgm/dragonatk.wav')
            Dragon.atk_sound.set_volume(12)

    def draw(self):
        if Dragon.image != None:
            Dragon.image[Dragon.state].draw(self.x, self.y, self.size_x, self.size_y)
        if Dragon.state == Dragon.ATK:
            Dragon.fire_img.draw(self.fire_x, self.fire_y, self.size_fire_x, self.size_fire_y)


    def update(self):
        Dragon.staycnt += 1
        if Dragon.state == Dragon.SLEEP_DOWN and chimmy.state == Chimmy.DOWN_FALL:
            Dragon.state = Dragon.SLEEP_UP
            self.size_x, self.size_y = 350, 180
        elif Dragon.state == Dragon.SLEEP_UP and chimmy.state == Chimmy.DOWN_STAND:
            Dragon.state = Dragon.WAKEUP
            self.size_x, self.size_y = 350, 360
            self.y += Map.BLOCKSIZE
        elif Dragon.state == Dragon.WAKEUP and chimmy.state == Chimmy.DOWN_FALL:
            Dragon.state = Dragon.FLY
            self.size_x, self.size_y = 350, 180
            Dragon.move_state = Dragon.M_UP
            #self.x = 800 + 180
        elif Dragon.state == Dragon.FLY and Dragon.staycnt == 100:
            Dragon.move_state = Dragon.M_LEFT
            self.x = 800 + 180
            self.y = chimmy.y
        elif Dragon.state == Dragon.FLY and self.x == -180:
            Dragon.state = Dragon.ATK
            self.size_x, self.size_y = 235, 360
            Dragon.move_state = Dragon.M_SLEEP
            self.x += 180 + position[0].x - Map.BLOCKSIZE
            #self.y -= Map.BLOCKSIZE * 2
            self.y = chimmy.y - Map.BLOCKSIZE * 2
        elif Dragon.state == Dragon.ATK:
            self.fire_y = self.y + Map.BLOCKSIZE * 2
            Dragon.move_state = Dragon.M_RIGHT

        Dragon.move(self)

    def move(self):
        #M_LEFT, M_RIGHT, M_UP, M_DOWN
        if not Dragon.M_SLEEP:
            Dragon.movecnt += 1

            if Dragon.move_state == Dragon.M_UP:
                self.y += Dragon.SPEED
                self.x -= Dragon.SPEED
                self.x = 800 + 180
                if Dragon.movecnt == 180:
                    Dragon.movecnt = 0
                    Dragon.move_state = Dragon.M_SLEEP
            elif Dragon.move_state == Dragon.M_DOWN:
                self.y -= Dragon.SPEED
                if Dragon.movecnt == 180:
                    Dragon.movecnt = 0
                    Dragon.move_state = Dragon.M_SLEEP
            elif Dragon.move_state == Dragon.M_LEFT:
                #제일 오른쪽으로 이동해서 왼쪽으로 이동
                self.x -= Dragon.SPEED * 4
                if self.x < -180:
                   self.x = 800 + 180
            elif Dragon.move_state == Dragon.M_RIGHT:
                Dragon.movecnt = 0
                #불 쏘기
                self.atk()
                if self.size_fire_x < position[3].x:
                    self.size_fire_x += Dragon.SPEED * 2
                    self.fire_x += Dragon.SPEED
                elif self.size_fire_x >= position[3].x:
                    self.size_fire_x = 0
                    self.fire_x = position[0].x
                    Dragon.state = Dragon.WAKEUP
                    self.size_x, self.size_y = 350, 360
                    Dragon.movecnt = 0
                    Dragon.move_state = Dragon.M_UP
                    self.x = 800 + 180

    def get_bb(self):
        return self.fire_x - (self.size_fire_x / 2) + 20, self.fire_y - (self.size_fire_y / 2) + 20\
            , self.fire_x + (self.size_fire_x / 2) - 20, self.fire_y + (self.size_fire_y / 2) - 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def atk(self):
        self.atk_sound.play()


class Chimmy:
    global position
    image = None
    LEFT_RUN, RIGHT_RUN, LEFT_ATK, RIGHT_ATK, DOWN_FALL, LEFT_STAND, RIGHT_STAND, DOWN_STAND, DEAD = 0, 1, 2, 3, 4, 5, 6, 7, 8

    speed = 3
    movecnt = 0
    size = 70
    cnt_max = 15
    state = RIGHT_STAND

    pos_row = 3
    pos_line = 4

    #sound
    break_sound = None

    #font
    score_font = None
    score = 0

    def __init__(self):
        self.state = Chimmy.RIGHT_STAND
        self.movecnt = 0
        Chimmy.pos_row = 3
        Chimmy.pos_line = 4

        self.x, self.y = position[Chimmy.pos_line * (Map.LINEMAX) + Chimmy.pos_row].x, position[Chimmy.pos_line * (Map.LINEMAX) + Chimmy.pos_row].y
        self.frame = 0
        if Chimmy.image == None:
            Chimmy.image = load_image('resource/character2.png')
        self.frame_h = 0
        self.cnt_frame = 0

        if Chimmy.break_sound == None:
            Chimmy.break_sound = load_wav('resource/bgm/wallbreak.wav')
            Chimmy.break_sound.set_volume(64)

        if Chimmy.score_font == None:
            Chimmy.score_font = load_font('resource/font/Blox2.ttf', 36)
        Chimmy.score = 0

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.DOWN_STAND):
                self.state = self.LEFT_RUN
                self.frame_h = self.LEFT_RUN
                self.cnt_frame = 0
                self.frame = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.DOWN_STAND):
                self.state = self.RIGHT_RUN
                self.frame_h = self.RIGHT_RUN
                self.cnt_frame = 0
                self.frame = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.DOWN_STAND):
                self.state = self.DOWN_FALL
                self.frame_h = self.DOWN_FALL
                self.cnt_frame = 0
                self.frame = 0
                Dragon.staycnt = 0
                if Dragon.state == Dragon.FLY:
                    Dragon.state = Dragon.WAKEUP
                    Dragon.movecnt = 0


    def update(self):
        global chimmy_dead, clear
        if self.state == self.RIGHT_RUN:
            if map_data[Chimmy.pos_line].state[Chimmy.pos_row + 1] == Map.WALL \
                    or map_data[Chimmy.pos_line].state[Chimmy.pos_row + 1] == Map.HINDRANCE:
                map_data[Chimmy.pos_line].state[Chimmy.pos_row + 1] = Map.EMPTY
                self.frame_h = Chimmy.RIGHT_ATK
                self.map_break()
                Chimmy.score += 1
                print("This is Right Wall ! \n")
            if map_data[Chimmy.pos_line].state[Chimmy.pos_row + 1] == Map.STONE:
                self.state = self.RIGHT_STAND
                print("This is Right Stone ! \n")
            else:
                self.x = min(position[5].x, self.x + Chimmy.speed)
                if self.movecnt + Chimmy.speed >= Map.BLOCKSIZE:
                    self.movecnt = Map.BLOCKSIZE
                elif self.movecnt + Chimmy.speed < Map.BLOCKSIZE:
                    self.movecnt = self.movecnt + Chimmy.speed
                self.cnt_frame = (self.cnt_frame + 1) % Chimmy.cnt_max
                if self.cnt_frame == 0:
                    self.frame = (self.frame + 1) % 5
                if self.movecnt >= Map.BLOCKSIZE:
                    self.state = self.RIGHT_STAND
                    self.movecnt = 0
                    self.frame = 0
                    Chimmy.pos_row += 1
                    if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.EMPTY:
                        self.state = Chimmy.DOWN_FALL
                        self.frame_h = Chimmy.DOWN_FALL
                    elif map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.HINDRANCE:
                        chimmy.state = Chimmy.DEAD
                        chimmy.frame_h = Chimmy.DEAD
                        chimmy_dead = True
                        print("collide Hindrance ! \n")
        elif self.state == self.LEFT_RUN:
            if map_data[Chimmy.pos_line].state[Chimmy.pos_row - 1] == Map.WALL \
                    or map_data[Chimmy.pos_line].state[Chimmy.pos_row - 1] == Map.HINDRANCE:
                map_data[Chimmy.pos_line].state[Chimmy.pos_row - 1] = Map.EMPTY
                self.frame_h = Chimmy.LEFT_ATK
                self.map_break()
                Chimmy.score += 1
                print("This is Left Wall ! \n")
            if map_data[Chimmy.pos_line].state[Chimmy.pos_row - 1] == Map.STONE:
                self.state = self.LEFT_STAND
                print("This is Left Block ! \n")
            else:
                self.x = max(position[1].x, self.x - Chimmy.speed)
                if self.movecnt + Chimmy.speed >= Map.BLOCKSIZE:
                    self.movecnt = Map.BLOCKSIZE
                elif self.movecnt + Chimmy.speed < Map.BLOCKSIZE:
                    self.movecnt = self.movecnt + Chimmy.speed
                self.cnt_frame = (self.cnt_frame + 1) % Chimmy.cnt_max
                if self.cnt_frame == 0:
                    self.frame = (self.frame + 1) % 5
                if self.movecnt >= Map.BLOCKSIZE:
                    self.state = self.LEFT_STAND
                    self.movecnt = 0
                    self.frame = 0
                    Chimmy.pos_row -= 1
                    if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.EMPTY:
                        self.state = Chimmy.DOWN_FALL
                        self.frame_h = Chimmy.DOWN_FALL
                    elif map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.HINDRANCE:
                        chimmy.state = Chimmy.DEAD
                        chimmy.frame_h = Chimmy.DEAD
                        chimmy_dead = True
                        print("collide Hindrance ! \n")
        elif self.state == self.DOWN_FALL:
            if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.WALL:
                map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] = Map.EMPTY
                self.map_break()
                Chimmy.score += 1
                print("This is Down Wall ! \n")
            if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.STONE:
                self.state = self.DOWN_STAND
                print("This is Down Stone ! \n")
            else:
                if self.movecnt + Chimmy.speed >= Map.BLOCKSIZE:
                    Map.DownCnt += Map.BLOCKSIZE - self.movecnt
                    if Dragon.pos_line <= 4:
                        dragon.y += Map.BLOCKSIZE - self.movecnt
                    self.movecnt = Map.BLOCKSIZE
                elif self.movecnt + Chimmy.speed < Map.BLOCKSIZE:
                    self.movecnt = self.movecnt + Chimmy.speed
                    Map.DownCnt += Chimmy.speed
                    if Dragon.pos_line <= 4:
                        dragon.y += Chimmy.speed
                self.cnt_frame = (self.cnt_frame + 1) % Chimmy.cnt_max
                if self.cnt_frame == 0:
                    self.frame = (self.frame + 1) % 5
                if self.movecnt >= Map.BLOCKSIZE:
                    Chimmy.pos_line += 1
                    if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] != Map.EMPTY \
                            and map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] != Map.HINDRANCE:
                        self.state = self.DOWN_STAND
                    elif map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.HINDRANCE:
                        chimmy.state = Chimmy.DEAD
                        chimmy.frame_h = Chimmy.DEAD
                        chimmy_dead = True
                        print("collide Hindrance ! \n")
                    self.movecnt = 0
                    self.frame = 0
                if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.CLEAR:
                    clear = True
                Dragon.staycnt = 0
                if Dragon.state == Dragon.ATK:
                    dragon.size_fire_x = 0
                    dragon.fire_x = position[0].x
                    Dragon.state = Dragon.WAKEUP
                    Dragon.movecnt = 0
                    Dragon.move_state = Dragon.M_UP
                    #dragon.x = 800 + 180

    def draw(self):
        self.image.clip_draw(self.frame * Chimmy.size, self.frame_h * Chimmy.size, Chimmy.size, Chimmy.size, self.x, self.y)
        Chimmy.score_font.draw(10, 560, 'score', (255, 255, 255))
        Chimmy.score_font.draw(10, 520, '%d' % Chimmy.score, (255, 255, 255))

    def get_bb(self):
        return self.x - (Map.BLOCKSIZE / 2) + 20, self.y - (Map.BLOCKSIZE / 2), self.x + (Map.BLOCKSIZE / 2) - 20, self.y + (Map.BLOCKSIZE / 2) - 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def map_break(self):
        self.break_sound.play()


def enter():
    global chimmy, background, map_data, map_next_data, stage1,stage_next, position, monster, monster_team, chimmy_dead, dragon
    global main_bgm, clear, firewall, firewall_team
    Map.DownCnt = 0
    Monster.mon_num = 0
    FireWall.firewall_num = 0
    monster_team = []
    firewall_team = []
    chimmy_dead = False
    clear = False

    background = BackGround()
    position = create_pos()
    map_data = create_map()
    stage1 = Map()
    chimmy = Chimmy()
    monster = Monster()
    firewall = FireWall()
    dragon = Dragon()

    main_bgm = load_music('resource/bgm/Go Go.mp3')
    main_bgm.set_volume(64)
    main_bgm.repeat_play()

def exit():
    global chimmy, background, map_data, stage1, position, monster_team, dragon, firewall_team
    global main_bgm
    del(chimmy)
    del(background)
    del(map_data)
    del(stage1)
    del(position)
    del(monster_team)
    del(firewall_team)
    del(dragon)
    main_bgm.stop()

def pause():
    pass

def resume():
    pass

def handle_events():
    global chimmy, map_data, bb_show
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_PLUS:
            if Chimmy.speed < 70:
                Chimmy.speed += 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_MINUS:
            if Chimmy.speed > 2:
                Chimmy.speed -= 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b:
            bb_show = not bb_show
        else:
            chimmy.handle_event(event)


def update():
    global chimmy_dead, clear

    if clear == True:
        game_framework.change_state(game_clear)
    elif chimmy_dead:
        game_framework.change_state(game_over)
    else:
        chimmy.update()
        stage1.update()
        monster.update_k()
        monster.update_t()
        dragon.update()
        firewall.update()

        # collide check
        if chimmy.state != Chimmy.DEAD:
            #chimmy and monster
            for m in monster_team:
                if collide(chimmy, m):
                    if chimmy.state == Chimmy.DOWN_FALL:
                        chimmy.state = Chimmy.DOWN_FALL
                        chimmy.frame_h = Chimmy.DOWN_FALL
                        monster_team.remove(m)
                        Monster.mon_num -= 1
                        Monster.die(m)
                        Chimmy.score += 5
                        print("collide Monster Die ! \n")
                    elif chimmy.state == Chimmy.LEFT_RUN or chimmy.state == Chimmy.LEFT_ATK:
                        if m.x < chimmy.x:
                            chimmy.frame_h = Chimmy.LEFT_ATK
                            monster_team.remove(m)
                            Monster.mon_num -= 1
                            Monster.die(m)
                            Chimmy.score += 5
                            print("collide Monster Die ! \n")
                    elif chimmy.state == Chimmy.RIGHT_RUN or chimmy.state == Chimmy.RIGHT_ATK:
                        if chimmy.x < m.x:
                            chimmy.frame_h = Chimmy.RIGHT_ATK
                            monster_team.remove(m)
                            Monster.mon_num -= 1
                            Monster.die(m)
                            Chimmy.score += 5
                            print("collide Monster Die ! \n")
                    else:
                        chimmy.state = Chimmy.DEAD
                        chimmy.frame_h = Chimmy.DEAD
                        chimmy_dead = True
                        print("collide ! \n")
            #chimmy and dragon fire
            if collide(chimmy, dragon):
                chimmy.state = Chimmy.DEAD
                chimmy.frame_h = Chimmy.DEAD
                chimmy_dead = True
                print("collide Fire ! \n")
            #chimmy and firewall fire
            for f in firewall_team:
                if f.fire_show == True:
                    if collide(chimmy, f):
                        chimmy.state = Chimmy.DEAD
                        chimmy.frame_h = Chimmy.DEAD
                        chimmy_dead = True
                        print("collide firewall Fire ! \n")


def draw_scene():
    background.draw(Chimmy.pos_line)
    if not Dragon.state == Dragon.SLEEP_DOWN or Dragon.state == Dragon.SLEEP_UP or Dragon.state == Dragon.ATK:
        dragon.draw()
    stage1.draw()
    if Dragon.state == Dragon.SLEEP_DOWN or Dragon.state == Dragon.SLEEP_UP or Dragon.state == Dragon.ATK:
        dragon.draw()
    chimmy.draw()
    monster.draw_k()
    monster.draw_t()
    firewall.draw()



def draw():
    clear_canvas()
    draw_scene()

   #  collide check box
    if bb_show:
        if chimmy.state != Chimmy.DEAD:
            chimmy.draw_bb()
        for m in monster_team:
            m.draw_bb()
        if Dragon.state == Dragon.ATK:
            dragon.draw_bb()
        for f in firewall_team:
            f.draw_bb()

    update_canvas()



def create_map():
    global position
    player_state_table = {
        "S": Map.STONE,
        "W": Map.WALL,
        "H": Map.HINDRANCE,
        "K": Map.MONSTER_K,
        "T": Map.MONSTER_T,
        "E": Map.EMPTY,
        "C": Map.CLEAR,
        "F": Map.FIREWALL,
        "N": None
    }

    stage1_file = open('stage1.txt', 'r')
    stage1 = json.load(stage1_file)
    stage1_file.close()

    stage2_file = open('stage2.txt', 'r')
    stage2 = json.load(stage2_file)
    stage2_file.close()

    map_data = stage1 + stage2

    map = []
    Map.rowcnt = 0

    for row_data in map_data:
        stage = Map()
        stage.row = row_data
        for i in range(Map.LINEMAX):
            stage.state.append(player_state_table[map_data[Map.rowcnt][i]])
            stage.randnum.append(random.randint(0, 4))

            if map_data[Map.rowcnt][i] == "K":
                append_monster(position[Map.rowcnt * (Map.LINEMAX) + i].x
                               , position[Map.rowcnt * (Map.LINEMAX) + i].y
                               , Map.MONSTER_K, Map.rowcnt, i)
            elif map_data[Map.rowcnt][i] == "T":
                append_monster(position[Map.rowcnt * (Map.LINEMAX) + i].x
                               , position[Map.rowcnt * (Map.LINEMAX) + i].y
                               , Map.MONSTER_T, Map.rowcnt, i)
            elif map_data[Map.rowcnt][i] == "F":
                append_firewall(position[Map.rowcnt * (Map.LINEMAX) + i].x
                               , position[Map.rowcnt * (Map.LINEMAX) + i].y
                               , Map.rowcnt, i)
        map.append(stage)
        Map.rowcnt += 1
    return map


def create_pos():
    pos_data_file = open('position2.txt', 'r')
    pos_data = json.load(pos_data_file)
    pos_data_file.close()

    position = []
    for key in pos_data:
        pos = Position()
        pos.key = key
        pos.x = 190 + (pos_data[key]['x'] * Map.BLOCKSIZE)
        pos.y = 570 - (pos_data[key]['y'] * Map.BLOCKSIZE)
        position.append(pos)

    return position


def append_monster(d_x, d_y, d_type, d_pos_row, d_pos_line):
    d_monster = Monster()
    d_monster.x = d_x
    d_monster.y = d_y
    d_monster.type = d_type
    d_monster.frame_cnt = 0
    d_monster.frame = random.randint(0, 3)
    d_monster.dir = random.randint(0, 1)
    d_monster.pos_row = d_pos_row
    d_monster.pos_line = d_pos_line
    monster_team.append(d_monster)
    Monster.mon_num += 1

def append_firewall(d_x, d_y, d_pos_row, d_pos_line):
    d_firewall = FireWall()
    d_firewall.x = d_x
    d_firewall.y = d_y
    d_firewall.pos_row = d_pos_row
    d_firewall.pos_line = d_pos_line
    firewall_team.append(d_firewall)
    FireWall.firewall_num += 1


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a >= right_b: return False
    if right_a <= left_b: return False
    if top_a <= bottom_b: return False
    if bottom_a > top_b: return False

    return True






