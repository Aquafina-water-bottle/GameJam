import os

import pygame

from sprites import Sprite, SpriteGroup

class Collectible(Sprite):
    display_names = {
        "bandages": "bandages",
        "bow_arrow": "a bow and arrow",
        "bread": "bread",
        "cheese": "cheese",
        "daggers": "daggers",
        "jerky": "beef jerky",
        "pileogold": "pile 'o gold",
        "sword": "a sword",
        "ugly_green_scarf": "ugly green scarf",
        "water_skin": "empty water skin",        # empty
        "filled_water_skin": "filled water skin",
    }

    def __init__(self, png_name, x, y, points, weight, type=None):
        if type is None:
            self.type = png_name.split(".")[0]
        else:
            self.type = type
        png_name = os.path.join("collectibles", png_name)
        super().__init__(png_name, x, y, convert_alpha=True)
        self.points = points
        self.weight = weight
        self.picked_up = False

    def collides(self, character, camera):
        return not self.picked_up and character.proper_size.colliderect(self.get_relative(camera))

    def pick_up(self):
        self.picked_up = True
        return Collectible.display_names[self.type]

    def draw(self, screen, camera):
        if not self.picked_up:
            super().draw(screen, camera)



