# import the pygame module, so you can use it
import os
import time

import pygame
from win import Win
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

- ending collide with box feet

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
        self.ambient = pygame.mixer.Sound("assets/ambient.wav")
        self.clock = pygame.time.Clock()
        self.countdown = Countdown()
        self.wins = []
        self.wins.append(Win(200 * SCALE, 280 * SCALE, 40 * SCALE, 20 * SCALE))
        self.wins.append(Win(400 * SCALE, 200 * SCALE, 60 * SCALE, 40 * SCALE))
        self.wins.append(Win(610 * SCALE, 330 * SCALE, 60 * SCALE, 20 * SCALE))

        self.collectibles = create_collectibles()
        self.buildings = create_buildings()
        self.ended = False
        self.fade_out_begin = -1

        # specifies the middle of the screen
        self.character = Character("MC-front.png", 0, 0)
        self.character.rect.x = SCREEN_SIZE[X]//2 - self.character.rect.width//2
        self.character.rect.y = SCREEN_SIZE[Y]//2 - self.character.rect.height//2

        self.user_input = UserInput()

        # TODO remove to add fade in
        self.fade_in = True
        self.fade_out = False
        #self.fade_in = False; self.countdown.start()  # because annoying

        # temporarily transforms the background to the current resolution
        self.default_background = load_image('BACKROUND.png', return_rect=False)

        self.building_wall_mask = load_image('background_outline3.png', convert_alpha=True, return_rect=False)
        # self.building_wall_mask = pygame.mask.from_surface(walls)

        # character mask is a literal constant one pixel at the base of the
        # self.character_mask = "deeznuts"

        # NOTE debugging purposes until mask is properly resized
        self.background = self.default_background
        #self.background = self.building_wall_mask

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
        while self.running and not self.ended:
            self.user_input.update()
            self.countdown.update()
            self.handle_event()
            self.draw()

            if self.continue_game and not self.fade_in:
                self.update()

            self.clock.tick(60)

        if self.ended:
            self.end()

    def handle_event(self):
        # checks if fading has end
        if self.fade_in and time.time() - begin_time > FADE_IN_TIME:
            self.fade_in = False
            self.countdown.start()
            self.ambient.play()

        if self.fade_out and time.time() - self.fade_out_begin > FADE_OUT_TIME:
            # self.fade_out = False
            self.ended = True

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
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (SCREEN_SIZE[X] // 2 - self.camera.x, SCREEN_SIZE[Y] // 2 - self.camera.y))
        # pygame.draw.rect(self.screen, color, self.character)

        # updates all collectibles only when "F" is pressed
        if self.user_input.clicked_interact(self.countdown.tick):
            self.collectibles.update(self.character, self.camera)

        # NOTE: TEMPORARY!!!
        #for building in self.buildings:
           # building.debug_draw_position(self.screen, self.camera)

        # draws sprites
        self.collectibles.draw(self.screen, self.camera)

        # draws debug
        for win in self.wins:
            win.debug_draw(self.camera, self.screen)

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

        if self.fade_out:
            # where alpha_value increases from 0 to 255
            alpha_value = int(255 * (time.time() - self.fade_out_begin) / FADE_OUT_TIME)
            black_fade_surface = self.screen.copy()
            black_fade_surface.fill(pygame.Color("black"))
            black_fade_surface.set_alpha(alpha_value)
            self.screen.blit(black_fade_surface, (0, 0))

        pygame.display.flip()


    def update(self):
        velocity = self.user_input.get_velocity()
        self.camera.store_previous()
        self.camera += velocity
        self.character.update(velocity, self.countdown.tick)

        # detects collision with walls and buildings
        pixel = (self.building_wall_mask.get_at(tuple(self.character.get_pixel_at_feet(self.camera))))
        if pixel[3] > ALPHA_THRESHOLD:
            # TODO move back character
            print("COLLIDES")
            self.camera.x = self.camera.previous_x
            self.camera.y = self.camera.previous_y
        else:
            print()

        if not self.in_building:
            # checks for the building shit
            for building in self.buildings:
                if building.enters(self.character, self.camera) and self.user_input.clicked_interact(self.countdown.tick):
                    self.in_building = True
                    self.current_building = building
                    self.background = self.current_building.background

                # collides with any win
                for win in self.wins:
                    if win.collide(self.camera, self.character):
                        self.continue_game = False
                        self.fade_out = True
                        self.fade_out_begin = time.time()
                        self.countdown.stop()
        else:
            # checks whether they have left the building
            pass

    def end(self):
        pass



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()




