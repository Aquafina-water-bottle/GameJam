import os

import pygame

def load_image(name):
    png_name = os.path.join('assets', name)
    image = pygame.image.load(png_name)
    image = image.convert()
    return image, image.get_rect()


class SpriteGroup:
    """
    wrapper to just draw and update all sprites at ocne
    """
    def __init__(self, sprite_dict):
        self._sprite_dict = sprite_dict

    def __getitem__(self, key):
        return self._sprite_dict[key]

    def draw(self, screen):
        for building in self._sprite_dict.values():
            building.draw(screen)

    def update(self, *args, **kwargs):
        """
        empty, can be changed
        """
        for building in self._sprite_dict.values():
            building.update(*args, **kwargs)

# def create_buildings():
#     buildings = {
#         "well": Well()
#     }
#
#     return Buildings(buildings)
#
# class SpriteGroup:
#     """
#     wrapper to just draw and update all buildings at once
#     """
#     def __init__(self, buildings_dict):
#         self._sprite_dict = buildings_dict
#
#     def __getitem__(self, key):
#         return self._sprite_dict[key]
#
#     def draw(self, screen):
#         for building in self._sprite_dict.values():
#             building.draw(screen)
#
#     def update(self, *args, **kwargs):
#         """
#         empty, can be changed
#         """
#         for building in self._sprite_dict.values():
#             building.update(*args, **kwargs)
#
# class Building:
#     """
#     assumes pictures are with format "<building_name>_top.png",
#     "<building_name>_bottom.png" under assets folder
#     """
#     def __init__(self, png_name, x, y, show_bottom=False):
#         self.background = IndividualBuilding(png_name + "_bottom.png", x, y)
#         self.show_bottom = show_bottom
#
#     def draw(self, screen):
#         if self.show_bottom:
#             self.bottom.draw(screen)
#         else:
#             self.top.draw(screen)
#
#     def update(self, *args, **kwargs):
#         """
#         empty, can be changed
#         """
#         self.bottom.update(*args, **kwargs)
#         self.top.update(*args, **kwargs)

class Sprite(pygame.sprite.Sprite):
    """
    TODO requires png transparency support for some reason idk
    """
    def __init__(self, png_name, x, y):
        self.image, self.rect = load_image(png_name)
        super().__init__()

        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, camera):
        relative_position = self.rect.copy()
        relative_position.x -= camera.x
        relative_position.y -= camera.y
        screen.blit(self.image, self.rect)


# class Well(Building):
#     def __init__(self):
#         super().__init__("well", 100, 60)
#
# class WatchTower:
#     pass
#
# class Butcher:
#     pass
#
# class Weaver:
#     pass
#
# class Baker:
#     pass
#
# class Player:
#     pass
#
# class NeighbourHouse:
#     pass

