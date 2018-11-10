import os

import pygame

def load_image(name):
    png_name = os.path.join('assets', name)
    image = pygame.image.load(png_name)
    image = image.convert()
    return image, image.get_rect()

def create_buildings():
    buildings = {
        "well": Well()
    }

    return buildings, pygame.sprite.Group(buildings.values())

class Building(pygame.sprite.Sprite):
    """
    TODO requires png transparency support for some reason idk
    """
    def __init__(self, png_name):
        self.image, self.rect = load_image(png_name)
        super().__init__()


class Well(Building):
    def __init__(self):
        super().__init__("well.png")

class WatchTower:
    pass

class Butcher:
    pass

class Weaver:
    pass

class Baker:
    pass

class Player:
    pass

class NeighbourHouse:
    pass

