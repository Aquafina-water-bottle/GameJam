import os

import pygame

from constants import *
from general import load_image, create_black_surface

class Button:
    def __init__(self, png_name, x_scale, y_scale, width_scale, height_scale, border_color):
        x = int(SCREEN_SIZE[X] * x_scale)
        y = int(SCREEN_SIZE[Y] * y_scale)
        width = int(SCREEN_SIZE[X] * width_scale)
        height = int(SCREEN_SIZE[Y] * height_scale)

        self.image = load_image(png_name, use_scale=False, return_rect=False)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.border = pygame.Rect(x, y, width, height)
        self.border_color = pygame.Color(border_color)

    def draw(self, screen):
        # draws border
        pygame.draw.rect(screen, self.border_color, self.border)

        # draws image button
        screen.blit(self.image, (self.border.x, self.border.y))


class MainMenu:
    def __init__(self, screen):
        self.background = load_image("main_menu.bmp", use_scale=False, return_rect=False)
        self.background = pygame.transform.scale(self.background, SCREEN_SIZE)
        self.black_surface = create_black_surface(screen)
        self.black_surface.set_alpha(100)
        self.play_button = Button("StartButton.bmp", 0.3, 0.4, 0.4, 0.15, "orange")
        self.exit_button = Button("QuitButton.bmp", 0.3, 0.57, 0.4, 0.15, "orange")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.black_surface, (0, 0))
        self.play_button.draw(screen)
        self.exit_button.draw(screen)


class PauseMenu:
    def __init__(self, screen):
        self.black_surface = create_black_surface(screen)
        self.black_surface.set_alpha(100)
        self.resume_button = Button("Resumebutton.bmp", 0.3, 0.4, 0.4, 0.15, "orange")
        self.exit_button = Button("QuitButton.bmp", 0.3, 0.57, 0.4, 0.15, "orange")

    def draw(self, screen):
        screen.blit(self.black_surface, (0, 0))
        self.resume_button.draw(screen)
        self.exit_button.draw(screen)



