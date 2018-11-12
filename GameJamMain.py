# import the pygame module, so you can use it
import os
import time
import pygame

from constants import *
from MainMenu import MainMenu
from win import create_wins
from countdown import Countdown
from building import create_buildings
from character import Character
from general import load_image, Coords
from user_input import UserInput

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

- get jared ssh lmao
"""

def main():
    running = True
    pygame.init()
    pygame.display.set_caption("Escape The Village")

    # create a surface on screen that has the size of 240 x 180144
    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)entrance
    screen = pygame.display.set_mode(SCREEN_SIZE)
    mainMenu = MainMenu(screen, SCREEN_SIZE)

    while running:
        mainMenu = MainMenu(screen, SCREEN_SIZE)
        game = Game(screen)
        if mainMenu.play():
            running = game.play()
        else:
            running = False

class Game:
    def __init__(self, screen):
        # initialize the pygame module
        self.screen = screen
        self.loop = True
        self.font = pygame.font.Font(None, 100)

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

        # creates the play and exit buttons
        self.play_button, self.play_image = make_continue_button()
        self.exit_button, self.exit_image = make_exit_button()

        self.ended = False
        self.fade_out_begin = -1
        self.begin_time = None

        # specifies the middle of the screen
        self.character = Character("avatar/MC-front.png", 0, 0)
        self.character.rect.x = SCREEN_SIZE[X]//2 - self.character.rect.width//2
        self.character.rect.y = SCREEN_SIZE[Y]//2 - self.character.rect.height//2

        self.user_input = UserInput()
        self.paused = False

        # TODO remove to add fade in
        self.fade_in = True
        self.fade_out = False
        #self.fade_in = False; self.countdown.start()  # because annoying

        # temporarily transforms the background to the current resolution
        self.default_background = load_image('background.png', return_rect=False)

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
        self.begin_time = time.time()
        self.ended = False
        self.fade_in = True
        self.beginning()
        while self.running and not self.ended:
            self.user_input.update()
            self.countdown.update()
            self.handle_event()
            self.draw()

            if self.paused:
                self.pause_update()
            elif self.continue_game and not self.fade_in:
                self.update()

            self.clock.tick(60)

        if self.ended:
            self.end()

        return self.running

        if DEBUG:
            print("debug: temp =", self.temp)
            print("collected {}".format(self.character.items))


    def handle_event(self):
        # checks if fading has end
        if self.fade_in and time.time() - self.begin_time > FADE_IN_TIME:
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

        if self.user_input.clicked_pause():
            self.countdown.pause()
            self.paused = True

    def beginning(self):
        self.screen.fill((0, 0, 0))


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
                self.current_building.debug_draw_inner(self.screen, self.camera)

            self.current_building.collectibles.draw(self.screen, self.camera)
            for collectible in self.current_building.collectibles:
                if self.character.proper_size.colliderect(collectible.get_relative(self.camera)) and self.user_input.clicked_interact(self.countdown.tick):
                    collectible.picked_up = True
                    self.character.items[collectible.type] += 1
                    self.character.points += collectible.points
                    self.character.weight += collectible.weight


        # draws countdown
        if not self.paused:
            self.countdown.draw(self.screen, self.font, self.fade_in)

        # draws character at the last lmao
        self.character.draw(self.screen)
        if DEBUG:
            self.character.draw_pixel(self.screen, self.camera)

        if self.fade_in:
            # where alpha_value decreases from 255 to 0
            alpha_value = int(255 - 255 * (time.time() - self.begin_time) / FADE_IN_TIME)
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

        if self.paused:
            # creates the dark shadow
            black_surface = self.screen.copy()
            black_surface.fill(pygame.Color("black"))
            black_surface.set_alpha(100)
            self.screen.blit(black_surface, (0, 0))

            pygame.draw.rect(self.screen, pygame.Color("orange"), self.play_button)
            self.screen.blit(self.play_image, (self.play_button.x, self.play_button.y))
            pygame.draw.rect(self.screen, pygame.Color("orange"), self.exit_button)
            self.screen.blit(self.exit_image, (self.exit_button.x, self.exit_button.y))

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

        # detects collision with walls and buildings
        pixel = (self.building_wall_mask.get_at(tuple(self.character.get_pixel_at_feet(self.camera))))
        if pixel[3] > ALPHA_THRESHOLD:
            # TODO move back character
            self.camera.x = self.camera.previous_x
            self.camera.y = self.camera.previous_y

        if not self.in_building:
            # detects collision with walls and buildings
            pixel = (self.building_wall_mask.get_at(tuple(self.character.get_pixel_at_feet(self.camera))))
            if pixel[3] > ALPHA_THRESHOLD:
                # TODO make less sticky if possible
                if COLLIDES:
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
                if COLLIDES:
                    self.camera.x = self.camera.previous_x
                    self.camera.y = self.camera.previous_y

            # detects collision for furinture
            for furniture in self.current_building.furniture.values():
                if furniture.rect.collidepoint(coords):
                    # TODO make less sticky if possible
                    if COLLIDES:
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

    def pause_update(self):
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self.play_button.collidepoint(pos):
                self.paused = False
            elif self.exit_button.collidepoint(pos):
                self.ended = True
                self.paused = False

        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            self.running = False
            self.paused = False

    def end(self):
        print("ended!")


def make_exit_button():
    exit_image = load_image("QuitButton.png", use_scale=True, return_rect=False)

    x = SCREEN_SIZE[0]
    y = SCREEN_SIZE[1]
    exit_x = int(x * 0.3)
    exit_width = int(x * 0.4)
    exit_y = int(y * 0.57)
    exit_height = int(y * 0.15)
    exit_image = pygame.transform.scale(exit_image, (exit_width, exit_height))

    return pygame.Rect(exit_x, exit_y, exit_width, exit_height), exit_image


def make_continue_button():
    play_image = load_image("Resumebutton.png", use_scale=True, return_rect=False)

    x = SCREEN_SIZE[0]
    y = SCREEN_SIZE[1]
    play_x = int(x * 0.3)
    play_width = int(x * 0.4)
    play_y = int(y * 0.4)
    play_height = int(y * 0.15)
    play_image = pygame.transform.scale(play_image, (play_width, play_height))

    return pygame.Rect(play_x, play_y, play_width, play_height), play_image


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
