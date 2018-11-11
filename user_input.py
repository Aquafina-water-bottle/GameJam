import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d, K_f, K_q

from constants import *
from general import Coords

class UserInput:
    """
    literally a wrapper class for getting the user input
    can be changed for controller input
    """
    def __init__(self):
        self.holding_interact = False
        self.tick = 0
        self.storage_tick = -1

    def update(self):
        self.pressed = pygame.key.get_pressed()
        self.tick += 1

    def clicked_quit(self):
        return self.pressed[K_q]

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

    def clicked_interact(self):
        # currently keyboard F

        # already calculated in the same frame
        if self.tick == self.storage_tick:
            return True

        # so that interact can be pressed once and not held down
        # since when it's held down, it will return false
        if self.pressed[K_f]:
            if not self.holding_interact:
                self.holding_interact = True
                self.storage_tick = self.tick
                return True
        else:
            self.holding_interact = False
        return False



