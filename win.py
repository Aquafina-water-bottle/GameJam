import pygame
from general import get_relative

class Win:
    def __init__(self, x, y, width, height):
        self.rectangle = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collide(self, camera, character):
        return character.rect.colliderect(get_relative(self.rectangle, camera))

    def debug_draw(self, camera, screen):
        relative_position = get_relative(self.rectangle, camera)
        pygame.draw.rect(screen, pygame.Color("green"), relative_position)
