import pygame
from sprites import *

class Building:
    """
    rect for collision, entrance
    image for background

    note that entrance is relative to position
    """
    def __init__(self, position, entrance, background_png_name):
        self.position = position
        self.entrance = pygame.Rect(entrance.x + position.x, entrance.y + position.y, entrance.width, entrance.height)
        self.background, _ = load_image(background_png_name)

    def get_relative(self, camera):
        relative_position = self.position.copy()
        relative_position.x += SCREEN_SIZE[X] // 2 - camera.x
        relative_position.y += SCREEN_SIZE[Y] // 2 - camera.y
        return relative_position

    def enters(self, camera):
        return self.entrance.collidepoint((camera.x, camera.y))

    def collides(self, character, camera):
        return character.colliderect(self.get_relative(camera))

    def _draw(self, screen, camera):
        """
        TEMPORARY
        """
        relative_position = self.get_relative(camera)
        screen.blit(self.background, relative_position)


def create_buildings():
    buildings_dict = {
        "main_house": Building(pygame.Rect(200, 300, 500, 500), pygame.Rect(100, 250, 50, 50), "sample_building.png"),
    }
    group = SpriteGroup(buildings_dict)
    return group

