# import the pygame module, so you can use it
import os
import time

import pygame
from win import win
from constants import *
from countdown import Countdown
from collectibles import create_collectibles
from building import create_buildings
from character import Character
from general import load_image, scale_surface, Coords
from user_input import UserInput

begin_time = time.time()

"""
TODO (programming):

- building mechanics:
    - enter buildings:
        - change background
        - load in collectibles
        - ability to exit building
    - bitmask

- collectible mechanics:
    - increment points to whatever

- character animations

- win condition
    - math for collectibles
    - areas for winning
"""

def main():
    game = Game()
    game.play()


class Game:
    def __init__(self):
        # initialize the pygame module
        pygame.init()
        self.font = pygame.font.Font(None, 100)
        pygame.display.set_caption("Escape The Village")

        # create a surface on screen that has the size of 240 x 180144
        # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)entrance
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        # define a variable to control the main loop
        self.running = True
        self.continue_game = True
        self.bell = pygame.mixer.Sound("assets/churchbell.wav")
        self.march = pygame.mixer.Sound("assets/marching.wav")
        self.clock = pygame.time.Clock()
        self.countdown = Countdown()
        self.win1 = win(200 * SCALE, 280 * SCALE, 40 * SCALE, 20 * SCALE)
        self.win2 = win(400 * SCALE, 200 * SCALE, 60 * SCALE, 40 * SCALE)
        self.win3 = win(610 * SCALE, 330 * SCALE, 60 * SCALE, 20 * SCALE)
        self.collectibles = create_collectibles()
        self.buildings = create_buildings()
        self.end = False

        # specifies the middle of the screen
        self.character = Character("MC-front.png", 0, 0)
        self.character.rect.x = SCREEN_SIZE[X]//2 - self.character.rect.width//2
        self.character.rect.y = SCREEN_SIZE[Y]//2 - self.character.rect.height//2

        self.user_input = UserInput()

        # TODO remove to add fade in
        self.fade_in = True
        #self.fade_in = False; self.countdown.start()  # because annoying

        # temporarily transforms the background to the current resolution
        self.default_background, _ = load_image('BACKROUND.png')
        self.walls = load_image('background_outline.png', return_rect=False)
        self.mask = pygame.mask.from_surface(self.walls)
        self.background = self.default_background

        # variables for when you're in some building
        self.in_building = False
        self.current_building = None

        self.camera = Coords(CHARACTER_START[X], CHARACTER_START[Y])

    # @property
    # def background(self):
    #     return self._background

    # @background.setter
    # def background(self, background):
    #     self._background = scale_surface(background)

    def play(self):
        self.bell.play(6)
        self.march.play()
        while self.running:
            self.user_input.update()
            self.countdown.update()
            self.handle_event()
            self.draw()
            if self.end:
                self.ended()
            if self.continue_game and not self.fade_in:
                self.update()
                print(self.camera)

            self.clock.tick(60)

    def handle_event(self):
        # checks if fading has ended
        if self.fade_in and time.time() - begin_time > FADE_IN_TIME:
            self.fade_in = False
            self.countdown.start()
            self.bell.play(5)
        # event handling, gets all event from the eventqueue
        event = pygame.event.poll()
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            self.running = False

        # checks if the countdown ends
        if not self.fade_in and self.countdown.get() <= 0:

            # can do stuff here idk
            self.continue_game = False

        if self.user_input.clicked_quit():
            self.running = False

    def draw(self):
        from general import get_relative
        color = (255, 100, 0)
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (SCREEN_SIZE[X] // 2 - self.camera.x, SCREEN_SIZE[Y] // 2 - self.camera.y))
        # pygame.draw.rect(self.screen, color, self.character)

        # updates all collectibles only when "F" is pressed
        if self.user_input.clicked_interact():
            self.collectibles.update(self.character, self.camera)

        # NOTE: TEMPORARY!!!
        #for building in self.buildings:
           # building.debug_draw_position(self.screen, self.camera)

        # draws sprites
        self.collectibles.draw(self.screen, self.camera)

        # draws countdown
        self.countdown.draw(self.screen, self.font, self.fade_in)

        # draws character at the last lmao
        self.character.draw(self.screen)

        if self.fade_in:
            # where alpha_value decreases from 255 to 0
            alpha_value = int(255 - 255 * (time.time() - begin_time) / FADE_IN_TIME)
            black_fade_surface = self.screen.copy()
            black_fade_surface.fill(pygame.Color("black"))
            black_fade_surface.set_alpha(alpha_value)
            self.screen.blit(black_fade_surface, (0, 0))
        pygame.display.flip()


    def update(self):
        pressed = pygame.key.get_pressed()
        velocity = self.user_input.get_velocity()
        self.camera += velocity
        self.character.update(velocity, self.countdown.tick)

        if not self.in_building:
            # checks for the building shit
            for building in self.buildings:
                if building.enters(self.character, self.camera) and self.user_input.clicked_interact():
                    self.in_building = True
                    self.current_building = building
                    self.background = self.current_building.background
                # TODO doesn't actually work lmao
                if self.win1.collide(self.camera, self.character):
                    self.end = True
        else:
            # checks whether they have left the building
            pass

    def ended(self):
        # where alpha_value decreases from 255 to 0
        alpha_value = int(255 * (time.time() - begin_time) / FADE_IN_TIME)
        black_fade_surface = self.screen.copy()
        black_fade_surface.fill(pygame.Color("black"))
        black_fade_surface.set_alpha(alpha_value)        
        self.continue_game = False
        



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()


                