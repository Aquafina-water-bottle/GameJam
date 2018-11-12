import os

import pygame

from constants import *
from sprites import SpriteGroup
from general import load_image, get_relative, Coords
from scaled_rect import ScaledRect
from collectibles import Collectible

class Building:
    """
    rect for collision, entrance
    image for background

    note that entrance is relative to position
    """
    def __init__(self, entrance, background_png_name, collectibles):
        png_name = os.path.join("inside_houses", background_png_name)
        self.entrance = ScaledRect.from_rect(entrance)
        self.background = load_image(png_name, return_rect=False)
        self.collectibles = collectibles

        exit_x = 59
        exit_y = self.background.get_height()//SCALE - 25
        exit_width = self.background.get_width()//SCALE - 59*2
        exit_height = 15
        self.exit_area = ScaledRect(exit_x, exit_y, exit_width, exit_height)
        self.walls = ScaledRect(11, 63, 140, 175)

    def enters(self, character, camera):
        return character.get_rect_at_feet().colliderect(get_relative(self.entrance.rect, camera))

    @property
    def camera_entrance_coords(self):
        """
        gets the camera into the middle of the entrance
        """
        return Coords(*self.entrance.rect.center)

    @property
    def camera_exit_coords(self):
        """
        gets the camera into the middle of the exit
        """
        return Coords(*self.exit_area.rect.center)

    def debug_draw_position(self, screen, camera):
        relative_position = get_relative(self.entrance.rect, camera)
        pygame.draw.rect(screen, pygame.Color("orange"), relative_position)

    def debug_draw_exit(self, screen, camera):
        relative_position = get_relative(self.walls.rect, camera)
        pygame.draw.rect(screen, pygame.Color("red"), relative_position)

        relative_position = get_relative(self.exit_area.rect, camera)
        pygame.draw.rect(screen, pygame.Color("orange"), relative_position)


def create_buildings():
    """
    964,990
    """
    buildings_dict = {
        "weaver_house": Building(
            entrance=pygame.Rect(323, 325, 20, 5),
            background_png_name="weaver_house.png",
            collectibles=SpriteGroup({
                "water_skin1": Collectible("water_skin.png", 20, 50, point_worth=5, weight=1)
            })
        ),
    }
    group = SpriteGroup(buildings_dict)
    return group

