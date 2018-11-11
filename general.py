from constants import *

def get_relative(rect, camera):
    relative_position = rect.copy()
    relative_position.x += SCREEN_SIZE[X] // 2 - camera.x
    relative_position.y += SCREEN_SIZE[Y] // 2 - camera.y
    return relative_position
