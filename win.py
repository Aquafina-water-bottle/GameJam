import pygame
from general import get_relative

class win:
    def __init__(self, x, y, width, height):
        self.rectangle = pygame.Rect(x, y, width, height) 
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collide(self, camera, character):
        return character.rect.colliderect(get_relative(self.rectangle, camera))
