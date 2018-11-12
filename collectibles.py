import os

import pygame

from sprites import Sprite, SpriteGroup

class Collectible(Sprite):
    def __init__(self, png_name, x, y, points, weight):
        self.type = png_name.split(".")[0]
        png_name = os.path.join("collectibles", png_name)
        super().__init__(png_name, x, y, convert_alpha=True)
        self.points = points
        self.weight = weight
        self.picked_up = False

    def update(self, character, camera):
        if not self.picked_up and character.rect.colliderect(self.get_relative(camera)):
            self.picked_up = True

    def draw(self, screen, camera):
        if not self.picked_up:
            super().draw(screen, camera)



