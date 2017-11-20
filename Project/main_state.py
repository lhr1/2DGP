import random
import json
import os

from pico2d import *

import game_framework
import title_state
from BackGround import BackGround
from Position import Position


name = "MainState"

background = None
chimmy = None
map_data = None
stage1 = None
position = None
monster_team = []
monster = None


class Map:
    global map_data, map_next_data, stage1, stage_next, position, monster_team
    imgSTONE, imgWALL, imgHINDRANCE, imgEMPTY = None, None, None, None
    STONE, WALL, HINDRANCE, MONSTER_K, MONSTER_T, EMPTY = 0, 1, 2, 3, 4, 5
    LINEMAX = 7
    ROWMAX = 60

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


    def update(self):
        pass


class Monster:
    global map_data, monster_team, position
    imgMONSTER_K, imgMONSTER_T = None, None
    mon_num = 0
    speed = 1

    def __init__(self):
        if Monster.imgMONSTER_K == None:
            Monster.imgMONSTER_K = load_image('resource/monster_suki.png')
        if Monster.imgMONSTER_T == None:
            Monster.imgMONSTER_T = load_image('resource/monster_tata.png')

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
            if monster_team[num].dir == 0:       #right
                if map_data[monster_team[num].pos_row].state[monster_team[num].pos_line + 1] ==  Map.EMPTY:
                    if map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line + 1] == Map.WALL \
                        or map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line + 1] == Map.STONE:
                        monster_team[num].x = min(position[monster_team[num].pos_line + 1].x, monster_team[num].x + Monster.speed)
                        monster_team[num].movecnt = monster_team[num].movecnt + Monster.speed
                        if monster_team[num].movecnt == Map.BLOCKSIZE:
                            monster_team[num].pos_line += 1
                            monster_team[num].movecnt = 0
                    else:
                        monster_team[num].dir = 1
                        monster_team[num].movecnt = 0
                else:
                    monster_team[num].dir = 1
                    monster_team[num].movecnt = 0
                    #if map_data[monster_team[num].pos_row].state[monster_team[num].pos_line - 1] ==  Map.EMPTY:
                    #    monster_team[num].dir = 0
            elif monster_team[num].dir == 1:       #left
                if map_data[monster_team[num].pos_row].state[monster_team[num].pos_line - 1] == Map.EMPTY:
                    if map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line - 1] == Map.WALL \
                        or map_data[monster_team[num].pos_row + 1].state[monster_team[num].pos_line - 1] ==  Map.STONE:
                        monster_team[num].x = max(position[monster_team[num].pos_line - 1].x, monster_team[num].x - Monster.speed)
                        monster_team[num].movecnt = monster_team[num].movecnt + Monster.speed
                        if monster_team[num].movecnt == Map.BLOCKSIZE:
                            monster_team[num].pos_line -= 1
                            monster_team[num].movecnt = 0
                    else:
                        monster_team[num].dir = 0
                        monster_team[num].movecnt = 0
                else:
                    monster_team[num].dir = 0
                    monster_team[num].movecnt = 0
                    #if map_data[monster_team[num].pos_row].state[monster_team[num].pos_line + 1] ==  Map.EMPTY:
                    #    monster_team[num].dir = 1


    def update_t(self):
        pass

    def get_bb(self):
        return self.x - (Map.BLOCKSIZE / 10), self.y - (Map.BLOCKSIZE / 2) + Map.DownCnt\
            , self.x + (Map.BLOCKSIZE / 10), self.y + (Map.BLOCKSIZE / 2) + Map.DownCnt

    def draw_bb(self):
        draw_rectangle(*self.get_bb())



class Chimmy:
    global position
    image = None
    LEFT_RUN, RIGHT_RUN, LEFT_ATK, RIGHT_ATK, DOWN_FALL, LEFT_STAND, RIGHT_STAND, DOWN_STAND, DEAD = 0, 1, 2, 3, 4, 5, 6, 7, 8

    speed = 2
    movecnt = 0
    size = 70
    cnt_max = 10
    state = RIGHT_STAND

    pos_row = 3
    pos_line = 4

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


    def update(self):
        if self.state == self.RIGHT_RUN:
            if map_data[Chimmy.pos_line].state[Chimmy.pos_row + 1] == Map.WALL \
                    or map_data[Chimmy.pos_line].state[Chimmy.pos_row + 1] == Map.HINDRANCE:
                map_data[Chimmy.pos_line].state[Chimmy.pos_row + 1] = Map.EMPTY
                self.frame_h = Chimmy.RIGHT_ATK
                print("This is Right Wall ! \n")
            if map_data[Chimmy.pos_line].state[Chimmy.pos_row + 1] == Map.STONE:
                self.state = self.RIGHT_STAND
                print("This is Right Stone ! \n")
            else:
                self.x = min(position[5].x, self.x + Chimmy.speed)
                self.movecnt = self.movecnt + Chimmy.speed
                self.cnt_frame = (self.cnt_frame + 1) % Chimmy.cnt_max
                if self.cnt_frame == 0:
                    self.frame = (self.frame + 1) % 5
                if self.movecnt == Map.BLOCKSIZE:
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
                        print("collide Hindrance ! \n")
        elif self.state == self.LEFT_RUN:
            if map_data[Chimmy.pos_line].state[Chimmy.pos_row - 1] == Map.WALL \
                    or map_data[Chimmy.pos_line].state[Chimmy.pos_row - 1] == Map.HINDRANCE:
                map_data[Chimmy.pos_line].state[Chimmy.pos_row - 1] = Map.EMPTY
                self.frame_h = Chimmy.LEFT_ATK
                print("This is Left Wall ! \n")
            if map_data[Chimmy.pos_line].state[Chimmy.pos_row - 1] == Map.STONE:
                self.state = self.LEFT_STAND
                print("This is Left Block ! \n")
            else:
                self.x = max(position[1].x, self.x - Chimmy.speed)
                self.movecnt = self.movecnt + Chimmy.speed
                self.cnt_frame = (self.cnt_frame + 1) % Chimmy.cnt_max
                if self.cnt_frame == 0:
                    self.frame = (self.frame + 1) % 5
                if self.movecnt == Map.BLOCKSIZE:
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
                        print("collide Hindrance ! \n")
        elif self.state == self.DOWN_FALL:
            if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.WALL:
                map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] = Map.EMPTY
                print("This is Down Wall ! \n")
            if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.STONE:
                self.state = self.DOWN_STAND
                print("This is Down Stone ! \n")
            else:
                self.movecnt = self.movecnt + Chimmy.speed
                Map.DownCnt += Chimmy.speed
                self.cnt_frame = (self.cnt_frame + 1) % Chimmy.cnt_max
                if self.cnt_frame == 0:
                    self.frame = (self.frame + 1) % 5
                if self.movecnt == Map.BLOCKSIZE:
                    Chimmy.pos_line += 1
                    if map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] != Map.EMPTY \
                            and map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] != Map.HINDRANCE:
                        self.state = self.DOWN_STAND
                    elif map_data[Chimmy.pos_line + 1].state[Chimmy.pos_row] == Map.HINDRANCE:
                        chimmy.state = Chimmy.DEAD
                        chimmy.frame_h = Chimmy.DEAD
                        print("collide Hindrance ! \n")

                    self.movecnt = 0
                    self.frame = 0



    def draw(self):
        self.image.clip_draw(self.frame * Chimmy.size, self.frame_h * Chimmy.size, Chimmy.size, Chimmy.size, self.x, self.y)

    def get_bb(self):
        return self.x - (Map.BLOCKSIZE / 2), self.y - (Map.BLOCKSIZE / 2), self.x + (Map.BLOCKSIZE / 2), self.y + (Map.BLOCKSIZE / 2)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def enter():
    global chimmy, background, map_data, map_next_data, stage1,stage_next, position, monster
    background = BackGround()
    position = create_pos()
    map_data = create_map()
    stage1 = Map()
    chimmy = Chimmy()
    monster = Monster()

def exit():
    global chimmy, background, map_data, stage1, position
    del(chimmy)
    del(background)
    del(map_data)
    del(stage1)
    del(position)


def pause():
    pass

def resume():
    pass

def handle_events():
    global chimmy, map_data
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        # 게임 오버 되고 다시 시작 초기화
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            #if chimmy.state == Chimmy.DEAD:
                Map.DownCnt = 0
                chimmy.__init__()
                Monster.mon_num = 0
                monster_team.clear()
                map_data.clear()
                map_data = create_map()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            chimmy.__init__()
            chimmy.state = Chimmy.DOWN_FALL
            chimmy.pos_row = 29
            chimmy.x, chimmy.y = position[Chimmy.pos_line * (Map.LINEMAX) + Chimmy.pos_row].x, position[Chimmy.pos_line * (Map.LINEMAX) + Chimmy.pos_row].y
            Map.DownCnt = 29 * Map.BLOCKSIZE
            Monster.mon_num = 0
        else:
            chimmy.handle_event(event)


def update():
    chimmy.update()
    stage1.update()
    monster.update_k()
    monster.update_t()

    # collide check
    if chimmy.state != Chimmy.DEAD:
        for m in monster_team:
            if collide(chimmy, m):
                if chimmy.state == Chimmy.DOWN_FALL:
                    chimmy.state = Chimmy.DOWN_FALL
                    chimmy.frame_h = Chimmy.DOWN_FALL
                    monster_team.remove(m)
                    Monster.mon_num -= 1
                    print("collide Monster Die ! \n")
                elif chimmy.state == Chimmy.LEFT_RUN or chimmy.state == Chimmy.LEFT_ATK:
                    if m.x < chimmy.x:
                        chimmy.frame_h = Chimmy.LEFT_ATK
                        monster_team.remove(m)
                        Monster.mon_num -= 1
                        print("collide Monster Die ! \n")
                elif chimmy.state == Chimmy.RIGHT_RUN or chimmy.state == Chimmy.RIGHT_ATK:
                    if chimmy.x < m.x:
                        chimmy.frame_h = Chimmy.RIGHT_ATK
                        monster_team.remove(m)
                        Monster.mon_num -= 1
                        print("collide Monster Die ! \n")
                else:
                    chimmy.state = Chimmy.DEAD
                    chimmy.frame_h = Chimmy.DEAD
                    print("collide ! \n")


def draw_scene():
    background.draw()
    stage1.draw()
    chimmy.draw()
    monster.draw_k()
    monster.draw_t()


def draw():
    clear_canvas()
    draw_scene()

    # collide check box
    #if chimmy.state != Chimmy.DEAD:
    #    chimmy.draw_bb()
    #for m in monster_team:
    #    m.draw_bb()

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
                append_monster(position[Map.rowcnt * (Map.LINEMAX) + i].x, position[Map.rowcnt * (Map.LINEMAX) + i].y, Map.MONSTER_K, Map.rowcnt, i)
            elif map_data[Map.rowcnt][i] == "T":
                append_monster(position[Map.rowcnt * (Map.LINEMAX) + i].x, position[Map.rowcnt * (Map.LINEMAX) + i].y, Map.MONSTER_T, Map.rowcnt, i)

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
        pos.x = 190 + (pos_data[key]['x'] * 70)
        pos.y = 570 - (pos_data[key]['y'] * 70)
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
    d_monster.pos_line =  d_pos_line
    monster_team.append(d_monster)
    Monster.mon_num += 1


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a >= right_b: return False
    if right_a <= left_b: return False
    if top_a <= bottom_b: return False
    if bottom_a > top_b: return False

    return True






