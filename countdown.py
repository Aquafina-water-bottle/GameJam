import time
import pygame

beginning_time = time.time()
COUNTDOWN_START = 5

def get_countdown():
    current_time = time.time()
    countdown = COUNTDOWN_START - (current_time - beginning_time)
    return countdown

def draw_countdown(screen, font):
    # countdown = round(get_countdown(), 2)

    if get_countdown() < 0:
        countdown = 0
    else:
        countdown = int(get_countdown()) + 1

    rendered_line = str(countdown)
    text_render = font.render(rendered_line, True, pygame.Color("white"))
    text_pos = text_render.get_rect()
    text_pos.topright = screen.get_rect().topright
    screen.blit(text_render, text_pos)





