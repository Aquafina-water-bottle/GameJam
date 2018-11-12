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
    def __init__(self, entrance, background_png_name, name, collectibles, furniture):
        png_name = os.path.join("inside_houses", background_png_name)
        self.entrance = ScaledRect.from_rect(entrance)
        self.background = load_image(png_name, return_rect=False)
        self.name = name
        self.collectibles = collectibles
        self.furniture = {k: ScaledRect.from_rect(v) for k, v in furniture.items()}

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

    def debug_draw_inner(self, screen, camera):
        relative_position = get_relative(self.walls.rect, camera)
        pygame.draw.rect(screen, pygame.Color("red"), relative_position)

        for furniture in self.furniture.values():
            relative_position = get_relative(furniture.rect, camera)
            pygame.draw.rect(screen, pygame.Color("green"), relative_position)

        relative_position = get_relative(self.exit_area.rect, camera)
        pygame.draw.rect(screen, pygame.Color("orange"), relative_position)


def create_buildings():
    """
    """
    buildings_dict = {
        "weaver_house": Building(
            entrance=pygame.Rect(323, 324, 20, 7),
            background_png_name="weaver_house.bmp",
            name="the weaver's house",
            collectibles=SpriteGroup({
                "bandages": Collectible("bandages.bmp", 37, 198),
                "scarf": Collectible("ugly_green_scarf.bmp", 44, 108),
            }),
            furniture={
                "thread_thing1": pygame.Rect(70, 65, 18, 23),
                "thread_thing2": pygame.Rect(98, 65, 21, 23),
                "thread_thing3": pygame.Rect(122, 203, 20, 24),
                "barrel": pygame.Rect(123, 56, 23, 30),
                "table": pygame.Rect(17, 179, 37, 45),
                "bed": pygame.Rect(14, 67, 44, 60),
            }
        ),

        "your_house": Building(
            entrance=pygame.Rect(518, 347, 20, 8),
            background_png_name="your_house.bmp",
            name="your house",
            collectibles=SpriteGroup({
                "gold": Collectible("pileogold.bmp", 39, 180)
            }),
            furniture={
                "bed": pygame.Rect(98, 65, 46, 66),
                "table": pygame.Rect(16, 179, 40, 46),
                "dresser": pygame.Rect(14, 58, 47, 27),
                "bedside_table": pygame.Rect(72, 56, 20, 29),
            }
        ),

        "other_house": Building(
            entrance=pygame.Rect(629, 500, 23, 8),
            background_png_name="other_house.bmp",
            name="the neighbour's house",
            collectibles=SpriteGroup({
                "sword": Collectible("sword.bmp", 37, 80),
                "bow and arrow": Collectible("bow_arrow.bmp", 130, 200),
                "daggers": Collectible("daggers.bmp", 100, 125),
            }),
            furniture={
                "bed": pygame.Rect(98, 58, 48, 97),
                "table": pygame.Rect(14, 62, 37, 45),
                "barrel1": pygame.Rect(15, 173, 21, 26),
                "barrel2": pygame.Rect(14, 204, 23, 28),
                "barrel3": pygame.Rect(41, 205, 23, 27),
                "barrel4": pygame.Rect(126, 203, 21, 29),

            }
        ),

        "baker_house": Building(
            entrance=pygame.Rect(449, 546, 22, 8),
            background_png_name="baker_house.bmp",
            name="the baker's house",
            collectibles=SpriteGroup({
                "bread": Collectible("bread.bmp", 19, 118),
                "cheese": Collectible("cheese.bmp", 37, 118),
            }),
            furniture={
                "ovens": pygame.Rect(33, 45, 114, 33),
                "dresser": pygame.Rect(16, 124, 98, 29),
                "barrels": pygame.Rect(125, 205, 23, 26),
            }
        ),

        "butcher_house": Building(
            entrance=pygame.Rect(307, 597, 20, 8),
            background_png_name="butcher_house.bmp",
            name="the butcher's house",
            collectibles=SpriteGroup({
                "water_skin": Collectible("water_skin.bmp", 38, 84),
                "jerky": Collectible("jerky.bmp", 19, 203),
            }),
            furniture={
                "table1": pygame.Rect(17, 68, 36, 44),
                "table2": pygame.Rect(104, 68, 36, 41),
                "dressers": pygame.Rect(17, 150, 96, 26),
                "small_table": pygame.Rect(15, 203, 19, 28),

            }
        ),

    }
    group = SpriteGroup(buildings_dict)
    return group

