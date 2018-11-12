import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d, K_f, K_q, K_t, K_ESCAPE, K_p

from constants import *
from general import Coords

class ClickedOnce:
    def __init__(self, *keys):
        self.keys = keys
        self.storage_tick = -1
        self.holding = False

    def clicked(self, tick, pressed):
        # currently keyboard F

        # already calculated in the same frame
        if tick == self.storage_tick:
            return True

        # so that interact can be pressed once and not held down
        # since when it's held down, it will return false
        if any(pressed[key] for key in self.keys):
            if not self.holding:
                self.holding = True
                self.storage_tick = tick
                return True
        else:
            self.holding = False
        return False





class UserInput:
    """
    literally a wrapper class for getting the user input
    can be changed for controller input
    """
    def __init__(self):
        self.click_once_interact = ClickedOnce(K_f)
        self.click_once_debug = ClickedOnce(K_t)
        self.click_once_pause = ClickedOnce(K_ESCAPE, K_p)

    def update(self):
        self.pressed = pygame.key.get_pressed()
        self.event = pygame.event.poll()

    def clicked_mouse(self):
        return self.event.type == pygame.MOUSEBUTTONUP and self.event.button == 1

    def clicked_quit(self):
        return self.pressed[K_q] or self.event.type == pygame.QUIT

    def get_velocity(self):
        """
        for the controller, can use trig here instead
        """
        velocity = Coords(0, 0)
        if self.pressed[K_UP] or self.pressed[K_w]:
            velocity.y -= VELOCITY
        if self.pressed[K_DOWN] or self.pressed[K_s]:
            velocity.y += VELOCITY

        if self.pressed[K_LEFT] or self.pressed[K_a]:
            velocity.x -= VELOCITY
        if self.pressed[K_RIGHT] or self.pressed[K_d]:
            velocity.x += VELOCITY

        return velocity

    def clicked_pause(self, tick):
        return self.click_once_pause.clicked(tick, self.pressed)

    def clicked_debug(self, tick):
        return self.click_once_debug.clicked(tick, self.pressed)

    def clicked_interact(self, tick):
        return self.click_once_interact.clicked(tick, self.pressed)

