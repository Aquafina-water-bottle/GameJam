import time
import pygame

COUNTDOWN_START = 60

class Countdown:
    def __init__(self):
        self.beginning_time = 0
        self.started = False
        self._tick = 0

    def start(self):
        self.started = True
        self.beginning_time = time.time()

    def update(self):
        if self.started:
            self._tick += 1

    @property
    def tick(self):
        """
        tick shouldn't be set m29
        """
        return self._tick

    def get(self):
        current_time = time.time()
        countdown = COUNTDOWN_START - (current_time - self.beginning_time)
        return countdown

    def draw(self, screen, font, fade_in):
        # countdown = round(get_countdown(), 2)

        if fade_in:
            countdown = COUNTDOWN_START
        elif self.get() < 0:
            countdown = 0
        else:
            countdown = int(self.get()) + 1

        rendered_line = str(countdown)
        text_render = font.render(rendered_line, True, pygame.Color("white"))
        text_pos = text_render.get_rect()
        text_pos.topright = screen.get_rect().topright
        screen.blit(text_render, text_pos)




