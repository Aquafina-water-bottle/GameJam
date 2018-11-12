import pygame
import os

class MainMenu:
    def __init__(self, screen, SCREEN_SIZE):
        self.screen = screen
        self.SCREEN_SIZE = SCREEN_SIZE
        self.background = pygame.image.load(os.path.join('assets/background.png'))
        self.background = pygame.transform.scale(self.background, (SCREEN_SIZE))
        self.black_surface = self.screen.copy()
        self.black_surface.fill(pygame.Color("black"))
        self.black_surface.set_alpha(100)
        self.running = True
        self.play_selected = False
        self.play_button, self.play_image, self.play_x, self.play_y = self.make_play_button()
        self.exit_button, self.exit_image, self.exit_x, self.exit_y = self.make_exit_button()

    def play(self):
        while self.running and not self.play_selected:
            self.handle_event()
            self.draw()
        return self.running

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.black_surface, (0,0))
        pygame.draw.rect(self.screen, pygame.Color("orange"), self.play_button)
        self.screen.blit(self.play_image, (self.play_x, self.play_y))
        pygame.draw.rect(self.screen, pygame.Color("orange"), self.exit_button)
        self.screen.blit(self.exit_image, (self.exit_x, self.exit_y))
        pygame.display.flip()

    def handle_event(self):
        # event handling, gets all event from the eventqueue
        event = pygame.event.poll()
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            self.running = False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            self.running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self.play_button.collidepoint(pos):
                self.play_selected = True
            elif self.exit_button.collidepoint(pos):
                self.running = False


    def make_play_button(self):
        play_image = pygame.image.load(os.path.join('assets/start button .png'))
        x = self.SCREEN_SIZE[0]
        y = self.SCREEN_SIZE[1]
        play_x = int(x * 0.3)
        play_width = int(x * 0.4)
        play_y = int(y * 0.4)
        play_height = int(y * 0.15)
        play_image = pygame.transform.scale(play_image, (play_width, play_height))
        return pygame.Rect(play_x, play_y, play_width, play_height), play_image, play_x, play_y

    def make_exit_button(self):
        exit_image = pygame.image.load(os.path.join('assets/quit button .png'))
        x = self.SCREEN_SIZE[0]
        y = self.SCREEN_SIZE[1]
        exit_x = int(x * 0.3)
        exit_width = int(x * 0.4)
        exit_y = int(y * 0.57)
        exit_height = int(y * 0.15)
        exit_image = pygame.transform.scale(exit_image, (exit_width, exit_height))
        return pygame.Rect(exit_x, exit_y, exit_width, exit_height), exit_image, exit_x, exit_y
