import game_framework
from pico2d import *

import start_state
import main_state
import game_over

open_canvas()
game_framework.run(main_state)
close_canvas()