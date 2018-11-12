import pygame

from general import get_relative, scale_rect
from constants import *

class ScaledRect:
    def __init__(self, x, y, width, height):
        self.rect = scale_rect(pygame.Rect(x, y, width, height))

    @classmethod
    def from_rect(cls, rect):
        return cls(rect.x, rect.y, rect.width, rect.height)

    def collide(self, camera, other):
        return other.colliderect(get_relative(self.rect, camera))

    def debug_draw(self, camera, screen, color="green"):
        relative_position = get_relative(self.rect, camera)
        pygame.draw.rect(screen, pygame.Color(color), relative_position)


