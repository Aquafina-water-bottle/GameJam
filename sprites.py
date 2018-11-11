import os

import pygame

from constants import *
from general import load_image


class SpriteGroup:
    """
    wrapper to just draw and update all sprites at ocne
    """
    def __init__(self, sprite_dict):
        self._sprite_dict = sprite_dict

    def __getitem__(self, key):
        return self._sprite_dict[key]

    def draw(self, screen, camera):
        for sprite in self._sprite_dict.values():
            sprite.draw(screen, camera)

    def __iter__(self):
        return iter(self._sprite_dict.values())

    def update(self, *args, **kwargs):
        """
        empty, can be changed
        """
        for sprite in self._sprite_dict.values():
            sprite.update(*args, **kwargs)


class Sprite(pygame.sprite.Sprite):
    """
    TODO requires png transparency support for some reason idk
    """
    def __init__(self, png_name, x, y, convert_alpha=False):
        self.image, self.rect = load_image(png_name, convert_alpha)
        super().__init__()

        self.rect.x = x
        self.rect.y = y

    def get_relative(self, camera):
        relative_position = self.rect.copy()
        relative_position.x += SCREEN_SIZE[X] // 2 - camera.x
        relative_position.y += SCREEN_SIZE[Y] // 2 - camera.y
        return relative_position

    def draw(self, screen, camera):
        relative_position = self.get_relative(camera)
        screen.blit(self.image, relative_position)



