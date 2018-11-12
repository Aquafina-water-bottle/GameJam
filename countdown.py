import time
import pygame

from constants import *

# countdown state
CDS_STARTED = 0
CDS_PAUSED = 1
CDS_STOPPED = 2

class Countdown:
    def __init__(self):
        self.beginning_time = 0
        self.state = CDS_STOPPED
        self.storage = -1
        self._tick = 0
        self.paused_time = 0

    def start(self):
        self.state = CDS_STARTED
        self.beginning_time = time.time()

    def stop(self):
        self.storage = self.get()
        self.state = CDS_STOPPED

    def update(self):
        if self.state == CDS_STARTED:
            self._tick += 1

    @property
    def ended(self):
        return self.get() <= 0

    @property
    def tick(self):
        """
        tick shouldn't be set m29
        """
        return self._tick

    def get(self):
        """
        decrements from 60 to 0
        """
        if self.state in (CDS_STOPPED, CDS_PAUSED):
            return self.storage
        current_time = time.time()
        self.countdown = COUNTDOWN_START - (current_time - self.beginning_time)
        return self.countdown

    def draw(self, screen, font):
        # countdown = round(get_countdown(), 2)

        if self.get() < 0:
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
        self.storage = self.get()
        self.state = CDS_PAUSED

    def unpause(self):
        self.beginning_time += time.time() - self.paused_time
        self.state = CDS_STARTED




