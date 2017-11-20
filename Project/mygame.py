import game_framework
from pico2d import *

import start_state
import main_state

open_canvas()
game_framework.run(main_state)
close_canvas()