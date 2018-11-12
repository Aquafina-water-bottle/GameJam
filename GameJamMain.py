# import the pygame module, so you can use it
import os
import time

import pygame
from win import create_wins
from constants import *
from countdown import Countdown
from building import create_buildings
from character import Character
from general import load_image, Coords
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

        self.buildings = create_buildings()

        # in_building_entrance for exterior
        self.in_building_entrance = False

        # in_building_exit for interior
        self.in_building_exit = False

        self.wins = create_wins()

        self.ended = False
        self.fade_out_begin = -1

        # specifies the middle of the screen
        self.character = Character("avatar/MC-front.png", 0, 0)
        self.character.rect.x = SCREEN_SIZE[X]//2 - self.character.rect.width//2
        self.character.rect.y = SCREEN_SIZE[Y]//2 - self.character.rect.height//2

        self.user_input = UserInput()

        # TODO remove to add fade in
        self.fade_in = True
        self.fade_out = False
        #self.fade_in = False; self.countdown.start()  # because annoying

        # temporarily transforms the background to the current resolution
        self.default_background = load_image('BACKROUND.png', return_rect=False)

        self.building_wall_mask = load_image('background_outline.png', convert_alpha=True, return_rect=False)
        # self.building_wall_mask = pygame.mask.from_surface(walls)

        # character mask is a literal constant one pixel at the base of the
        # self.character_mask = "deeznuts"

        # NOTE debugging purposes until mask is properly resized
        self.background = self.default_background
        #self.background = self.building_wall_mask

        # variables for when you're in some building
        self.current_building = None

        self.camera = Coords(CHARACTER_START[X], CHARACTER_START[Y])
        self.camera_save = None

        self.temp = []

    # @property
    # def background(self):
    #     return self._background

    # @background.setter
    # def background(self, background):
    #     self._background = scale_surface(background)

    @property
    def in_building(self):
        return self.current_building is not None

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

        if DEBUG:
            print(self.temp)

    def handle_event(self):
        # checks if fading has end
        if self.fade_in and time.time() - begin_time > FADE_IN_TIME:
            self.fade_in = False
            self.countdown.start()
            if not DEBUG:
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
        if not self.fade_in and not self.fade_out and self.countdown.get() <= 0:
            # can do stuff here idk
            self.begin_fade_out()

        if self.user_input.clicked_quit():
            self.running = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (SCREEN_SIZE[X] // 2 - self.camera.x, SCREEN_SIZE[Y] // 2 - self.camera.y))
        # pygame.draw.rect(self.screen, color, self.character)

        if not self.in_building:
            if DEBUG:
                for building in self.buildings:
                    building.debug_draw_position(self.screen, self.camera)
                for win in self.wins:
                    win.debug_draw(self.camera, self.screen)

        else:
            if DEBUG:
                self.current_building.debug_draw_exit(self.screen, self.camera)
            self.current_building.collectibles.draw(self.screen, self.camera)


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
        if DEBUG:
            coords = self.character.get_pixel_at_feet(self.camera)
            print(coords)
            if self.user_input.clicked_debug(self.countdown.tick):
                self.temp.append(coords)
        self.character.update(velocity, self.countdown.tick)

        if not self.in_building:
            # detects collision with walls and buildings
            pixel = (self.building_wall_mask.get_at(tuple(self.character.get_pixel_at_feet(self.camera))))
            if pixel[3] > ALPHA_THRESHOLD:
                # TODO make less sticky if possible
                if not DEBUG:
                    self.camera.x = self.camera.previous_x
                    self.camera.y = self.camera.previous_y

            # checks for the building shit
            for building in self.buildings:
                if building.enters(self.character, self.camera) and self.user_input.clicked_interact(self.countdown.tick):
                    self.current_building = building
                    self.background = building.background
                    self.camera_save = self.camera.copy()

                    # resets the camera
                    building_exit_coords = building.camera_exit_coords
                    building_exit_coords.y -= self.character.rect.height // 2
                    self.camera = building_exit_coords

                # collides with any win
                for win in self.wins:
                    if win.collide(self.camera, self.character.get_rect_at_feet()):
                        self.begin_fade_out()

        else:
            # detects collision with the building walls by checking
            # if the player leaves the given rect
            coords = tuple(self.character.get_pixel_at_feet(self.camera))
            if not self.current_building.walls.rect.collidepoint(coords):
                # TODO make less sticky if possible
                if not DEBUG:
                    self.camera.x = self.camera.previous_x
                    self.camera.y = self.camera.previous_y


            # checks whether they have left the building
            if (self.current_building.exit_area.collide(self.camera, self.character.get_rect_at_feet())
                    and self.user_input.clicked_interact(self.countdown.tick)):
                self.camera = self.camera_save
                self.current_building = None
                self.background = self.default_background
                self.in_building_entrance = True

    def begin_fade_out(self):
        self.continue_game = False
        self.fade_out = True
        self.fade_out_begin = time.time()
        self.countdown.stop()

    def end(self):
        pass



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()




