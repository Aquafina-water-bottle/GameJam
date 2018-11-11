import pygame

from constants import *
from sprites import SpriteGroup
from general import load_image, get_relative

class Building:
    """
    rect for collision, entrance
    image for background

    note that entrance is relative to position
    """
    def __init__(self, position, entrance, exit_area, background_png_name):
        self.position = position
        self.entrance = pygame.Rect(entrance.x + position.x, entrance.y + position.y, entrance.width, entrance.height)
        self.exit_area = pygame.Rect(exit_area.x*SCALE, exit_area.y, exit_area.width, exit_area.height)
        self.background, _ = load_image(background_png_name)

    def enters(self, character, camera):
        return character.rect.colliderect(get_relative(self.entrance, camera))

    def collides(self, character, camera):
        return character.rect.colliderect(get_relative(self.position, camera))

    @property
    def camera_entrance_outer(self):
        """
        gets the camera into the middle of the entrance
        """
        pass

    @property
    def camera_entrance_inner(self):
        pass

    def debug_draw_position(self, screen, camera):
        relative_position = get_relative(self.position, camera)
        pygame.draw.rect(screen, pygame.Color("green"), relative_position)
        # screen.blit(self.background, relative_position)

        relative_position = get_relative(self.entrance, camera)
        pygame.draw.rect(screen, pygame.Color("orange"), relative_position)


def create_buildings():
    buildings_dict = {
        "main_house": Building(
            position=pygame.Rect(500, 500, 500, 500),
            entrance=pygame.Rect(250, 450, 50, 50),
            exit_area=pygame.Rect(250, 450, 50, 50),
            background_png_name="sample_building2.png"
        ),
    }
    group = SpriteGroup(buildings_dict)
    return group

