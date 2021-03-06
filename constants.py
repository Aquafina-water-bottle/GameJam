WIDTH = X = 0
HEIGHT = Y = 1

SCALE = 4
VELOCITY = 4

DEBUG = 0
COLLIDES = 1

# MAP_SIZE = (640*SCALE, 640*SCALE)
# TOWN_SIZE = (1280, 1280)
# TODO make borders at some point, probably doesn't need town size
SCREEN_SIZE = (640, 640)
CHARACTER_START = (526*SCALE, 360*SCALE)

RUNNING_ANIMATION_DELAY = 15

ALPHA_THRESHOLD = 151

INTERACT_KEY = "F"


FEET_HEIGHT = 4
FEET_WIDTH_REMOVE_SIDES = 6


# time delay for sounds in milliseconds
AMBIENT_FADE_OUT = 5000

# duration for the text on the bottom left corner
NOTIFICATION_TIME = 1


# time delays for all fade in and display, etc
MAIN_MENU_FADE_IN_TIME = 1.5
MAIN_MENU_FADE_OUT_TIME = 1

BEGIN_FADE_IN_TIME = 1
BEGIN_DISPLAY_TIME = 10
BEGIN_FADE_OUT_TIME = 1

GAME_FADE_IN_TIME = 3
COUNTDOWN_START = 60
GAME_FADE_OUT_TIME = 2.2

END_FADE_IN_TIME = 2.2
END_DISPLAY_TIME = 10
END_FADE_OUT_TIME = 2.2



# All states
# Note that this does not include state changes
# as all of those will be methods in the Game class
MAIN_MENU_FADE_IN = -1      # I'm way too lazy to change this to 0
MAIN_MENU = 0
MAIN_MENU_FADE_OUT = 1

BEGIN_FADE_IN = 2
BEGIN_DISPLAY = 3
BEGIN_FADE_OUT = 4

GAME_FADE_IN = 5
GAME_PLAY = 6
GAME_PAUSE = 7
GAME_FADE_OUT = 8

END_FADE_IN = 9
END_DISPLAY = 10
END_FADE_OUT = 11

STATE_DICT = {
    -1: "MAIN_MENU_FADE_IN",
    0: "MAIN_MENU",
    1: "MAIN_MENU_FADE_OUT",
    2: "BEGIN_FADE_IN",
    3: "BEGIN_DISPLAY",
    4: "BEGIN_FADE_OUT",
    5: "GAME_FADE_IN",
    6: "GAME_PLAY",
    7: "GAME_PAUSE",
    8: "GAME_FADE_OUT",
    9: "END_FADE_IN",
    10: "END_DISPLAY",
    11: "END_FADE_OUT",
}

# Combinations of states
STATES_FADE_IN = frozenset({MAIN_MENU_FADE_IN, BEGIN_FADE_IN, GAME_FADE_IN, END_FADE_IN})
STATES_FADE_OUT = frozenset({MAIN_MENU_FADE_OUT, BEGIN_FADE_OUT, GAME_FADE_OUT, END_FADE_OUT})
STATES_DISPLAY = frozenset({BEGIN_DISPLAY, END_DISPLAY})



