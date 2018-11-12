import time
import pygame

from constants import *

class Countdown:
    def __init__(self):
        self.beginning_time = 0
        self.started = False
        self.stopped = False
        self.storage = -1
        self._tick = 0
        self.paused_time = 0

    def start(self):
        self.started = True
        self.beginning_time = time.time()

    def stop(self):
        self.storage = self.get()
        self.stopped = True

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
        if self.stopped:
            return self.storage
        current_time = time.time()
        self.countdown = COUNTDOWN_START - (current_time - self.beginning_time)
        return self.countdown

    def draw(self, screen, font, fade_in):
        # countdown = round(get_countdown(), 2)

        if fade_in:
            countdown = COUNTDOWN_START
        elif self.get() < 0:
            countdown = 0
        else:
            countdown = int(self.get()) + 1

        rendered_line = str(countdown)
        text_render = font.render(rendered_line, True, pygame.Color("orange"))
        text_pos = text_render.get_rect()
        text_pos.topright = screen.get_rect().topright
        screen.blit(text_render, text_pos)

    def pause(self):
        self.paused_time = time.time()

    def unpause(self):
        self.beginning_time += time.time() - self.paused_time




