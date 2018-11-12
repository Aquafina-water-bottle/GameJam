import os

import pygame

from constants import *

def get_relative(rect, camera):
    """
    gets position relative to the camera
    """
    relative_position = rect.copy()
    relative_position.x += SCREEN_SIZE[X] // 2 - camera.x
    relative_position.y += SCREEN_SIZE[Y] // 2 - camera.y
    return relative_position

def scale_rect(rect):
    return pygame.Rect(rect.x*SCALE, rect.y*SCALE, rect.width*SCALE, rect.height*SCALE)

def scale_surface(surface):
    new_resolution = (surface.get_width()*SCALE, surface.get_height()*SCALE)
    return pygame.transform.scale(surface, new_resolution)

def create_black_surface(screen):
    black_surface = screen.copy()
    black_surface.fill(pygame.Color("black"))
    return black_surface

def load_image(name, convert_alpha=False, use_scale=True, flip=False, return_rect=True):
    png_name = os.path.join('assets', name)
    image = pygame.image.load(png_name)
    if use_scale:
        image = scale_surface(image)

    if convert_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if flip:
        image = pygame.transform.flip(image, True, False)

    if return_rect:
        return image, image.get_rect()
    return image

class Coords:
    """
    Temporary class to store coordinates

    Should replace this with some character class or rect object or something lmao
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.previous_x = X
        self.previous_y = y

    def copy(self):
        return Coords(self.x, self.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        return NotImplemented

    def __repr__(self):
        return "Coords(x={}, y={})".format(self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other):
        if not isinstance(other, Coords):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    def store_previous(self):
        self.previous_x = self.x
        self.previous_y = self.y

