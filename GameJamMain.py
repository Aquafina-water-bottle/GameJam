# import the pygame module, so you can use it
import os
import time
import pygame

from constants import *
from menu import MainMenu, PauseMenu
from win import create_wins
from countdown import Countdown
from building import create_buildings
from character import Character
from general import load_image, Coords
from user_input import UserInput
from timer import Timer, Ticker

"""
TODO (programming):
- get jared ssh lmao

- win condition (discuss balancing)
    - math for collectibles

- fade in and out literally everything
    - 

- show ending and actually fade in and fade out ending
- load sample image for beginning

- pick up item: text
- both exit and entering: text
    - both show up for 1 second

- well to get water
"""

def main():
    game = Game()
    game.play()

class Game:
    def __init__(self):
        # initialize the pygame module
        pygame.init()
        pygame.display.set_caption("Escape The Village")
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.black_surface = self.screen.copy()
        self.black_surface.fill(pygame.Color("black"))

        # default font used for the timer
        self.font = pygame.font.Font(None, 100)

        # define a variable to control the main loop
        # where it is really only set to false if the player exits or the X button is pressed
        self.running = True
        self.continue_game = True
        self.state = MAIN_MENU

        self.ambient = pygame.mixer.Sound("assets/ambient.wav")
        self.clock = pygame.time.Clock()
        self.countdown = Countdown()
        self.ticker = Ticker()

        self.buildings = create_buildings()

        self.wins = create_wins()

        # self.ended = False
        # self.show_ending = False

        self.end_image = None
        self.begin_image = load_image("begin_temp.png", use_scale=False, return_rect=False)
        self.begin_image = pygame.transform.scale(self.begin_image, SCREEN_SIZE)

        # self.fade_out_begin = -1
        # self.begin_time = None
        self.fade_in_timer = Timer()
        self.display_timer = Timer()
        self.fade_out_timer = Timer()

        # specifies the middle of the screen
        self.character = Character("avatar/MC-front.png", 0, 0)

        self.user_input = UserInput()
        # self.paused = False

        # TODO remove to add fade in
        # self.fade_in = True
        # self.fade_out = False
        #self.fade_in = False; self.countdown.start()  # because annoying

        self.default_background = load_image('background.png', return_rect=False)
        self.building_wall_mask = load_image('background_outline.png', convert_alpha=True, return_rect=False)

        # background can change to default background or house background
        self.background = self.default_background

        # creates the start menus
        self.pause_menu = PauseMenu(self.screen)
        self.main_menu = MainMenu(self.screen, self.background)

        # variables for when you're in some building
        self.current_building = None

        self.camera = Coords(CHARACTER_START[X], CHARACTER_START[Y])

        # saves the camera for when enering the building
        self.camera_save = None

        self.temp = []

    @property
    def in_building(self):
        return self.current_building is not None

    def play(self):
        while self.running:
            print(STATE_DICT[self.state])
            self.handle_event()
            self.draw()
            self.update()

            self.clock.tick(60)

        # if self.ended:
        #     self.get_end_image()

        # return self.running

        if DEBUG:
            print("debug: temp =", self.temp)
            print("collected {}".format(self.character.items))

    def handle_event(self):
        self.user_input.update()
        self.ticker.update()

        # checks for pause menu clicks
        if self.state == GAME_PAUSE and self.user_input.clicked_mouse():
            pos = pygame.mouse.get_pos()
            if self.pause_menu.resume_button.border.collidepoint(pos):
                self.state = GAME_PLAY
                self.countdown.unpause()
            if self.pause_menu.exit_button.border.collidepoint(pos):
                self.running = False

        # checks for main menu clicks
        if self.state == MAIN_MENU and self.user_input.clicked_mouse():
            pos = pygame.mouse.get_pos()
            if self.main_menu.play_button.border.collidepoint(pos):
                print("BRUH")
                self.state = MAIN_MENU_FADE_OUT
                self.fade_out_timer.start(MAIN_MENU_FADE_OUT_TIME)
            if self.main_menu.exit_button.border.collidepoint(pos):
                self.running = False
                return

        # only do something if the event is of type QUIT
        if self.user_input.clicked_quit():
            # change the value to False, to exit the main loop
            self.running = False
            return

        if self.user_input.clicked_pause():
            self.countdown.pause()
            self.state = GAME_PAUSE

        # if the player presses interact and it's during one of the display screens
        if self.user_input.clicked_interact(self.ticker.tick):
            if BEGIN_FADE_IN <= self.state <= BEGIN_FADE_OUT:
                self.start_game_fade_in()

            if END_FADE_IN <= self.state <= END_FADE_OUT:
                self.to_main_menu()

        if self.state in STATES_DISPLAY:
            if self.display_timer.ended:
                if self.state == BEGIN_DISPLAY:
                    # begin display -> fade out begin display
                    self.state = BEGIN_FADE_OUT
                    self.fade_out_timer.start(BEGIN_FADE_OUT_TIME)

                elif self.state == END_DISPLAY:
                    # end display -> fade out end display
                    self.state = END_FADE_OUT
                    self.fade_out_timer.start(END_FADE_OUT_TIME)

        if self.state in STATES_FADE_IN:
            if self.fade_in_timer.ended:
                if self.state == BEGIN_FADE_IN:
                    # end instruction fade in
                    self.state = BEGIN_DISPLAY
                    self.display_timer.start(BEGIN_DISPLAY_TIME)

                elif self.state == GAME_FADE_IN:
                    # starts the game here (end fade in)
                    self.countdown.start()
                    self.ambient.play()
                    self.state = GAME_PLAY

                elif self.state == END_FADE_IN:
                    # end the ending fade in
                    self.state = END_DISPLAY
                    self.display_timer.start(END_DISPLAY_TIME)

        if self.state in STATES_FADE_OUT:
            if self.fade_out_timer.ended:
                if self.state == MAIN_MENU_FADE_OUT:
                    # menu fade out -> begin fade in
                    self.state = BEGIN_FADE_IN
                    self.fade_in_timer.start(BEGIN_FADE_IN_TIME)

                elif self.state == BEGIN_FADE_OUT:
                    # begin fade out -> game fade in
                    self.start_game_fade_in()

                elif self.state == GAME_FADE_OUT:
                    # already ended the game, shows display
                    self.state = END_FADE_IN
                    self.fade_in_timer.start(END_FADE_IN_TIME)

                elif self.state == END_FADE_OUT:
                    self.to_main_menu()

        # countdown ends: game ends
        if self.state == GAME_PLAY and self.countdown.ends:
            self.end()

    def draw(self):

        # fills black background for when you can see the edge of the map
        # like in houses
        self.screen.fill((0, 0, 0))

        # draws the background relative to the character and countdown
        if GAME_FADE_IN <= self.state <= GAME_FADE_OUT:
            self.screen.blit(self.background, (SCREEN_SIZE[X] // 2 - self.camera.x, SCREEN_SIZE[Y] // 2 - self.camera.y))

            self.countdown.draw(self.screen, self.font)

            if not self.in_building:
                if DEBUG:
                    for building in self.buildings:
                        building.debug_draw_position(self.screen, self.camera)
                    for win in self.wins:
                        win.debug_draw(self.camera, self.screen)

            else:
                # in building
                if DEBUG:
                    self.current_building.debug_draw_inner(self.screen, self.camera)

                # draws all collectibles within a building
                self.current_building.collectibles.draw(self.screen, self.camera)

            # draws character at the last lmao
            self.character.draw(self.screen)
            if DEBUG:
                self.character.draw_pixel(self.screen, self.camera)

            if self.state == GAME_PAUSE:
                self.pause_menu.draw(self.screen)

        # displays the beginning image
        if BEGIN_FADE_IN <= self.state <= BEGIN_FADE_OUT:
            self.screen.blit(self.begin_image, (0, 0))

        # displays the ending image
        if END_FADE_IN <= self.state <= END_FADE_OUT:
            self.screen.blit(self.end_image, (0, 0))

        # displays the main menu
        if self.state in (MAIN_MENU, MAIN_MENU_FADE_OUT):
            self.main_menu.draw(self.screen)

        if self.state in STATES_FADE_IN or self.state in STATES_FADE_OUT:
            if self.state in STATES_FADE_IN:
                # goes from black to normal
                alpha_value = int(255 * (self.fade_in_timer.get()))
            else:
                # goes from normal to black
                alpha_value = int(255 - 255 * (self.fade_out_timer.get()))

            self.black_surface.set_alpha(alpha_value)
            self.screen.blit(self.black_surface, (0, 0))

        pygame.display.flip()

    def update(self):

        if self.state == GAME_PLAY:
            self.countdown.update()

            velocity = self.user_input.get_velocity()
            self.camera.store_previous()
            self.camera += velocity
            if DEBUG:
                coords = self.character.get_pixel_at_feet(self.camera)
                print(coords)
                if self.user_input.clicked_debug(self.ticker.tick):
                    self.temp.append(coords)
            self.character.update(velocity, self.ticker.tick)

            # detects collision with walls and buildings
            pixel = (self.building_wall_mask.get_at(tuple(self.character.get_pixel_at_feet(self.camera))))
            if pixel[3] > ALPHA_THRESHOLD:
                # TODO move back character
                self.camera.x = self.camera.previous_x
                self.camera.y = self.camera.previous_y

            if self.user_input.clicked_interact(self.ticker.tick):
                print("clicked interact")
            else:
                print("")

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
                    if building.enters(self.character, self.camera) and self.user_input.clicked_interact(self.ticker.tick):
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
                        self.end()

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

                # checks for collectibles
                for collectible in self.current_building.collectibles:
                    if self.character.proper_size.colliderect(collectible.get_relative(self.camera)) and self.user_input.clicked_interact(self.ticker.tick):
                        collectible.picked_up = True
                        self.character.items[collectible.type] += 1
                        self.character.points += collectible.points
                        self.character.weight += collectible.weight

                # checks whether they have left the building
                if (self.current_building.exit_area.collide(self.camera, self.character.get_rect_at_feet())
                        and self.user_input.clicked_interact(self.ticker.tick)):
                    self.camera = self.camera_save
                    self.current_building = None
                    self.background = self.default_background

    def start_game_fade_in(self):
        self.state = GAME_FADE_IN
        self.fade_in_timer.start(GAME_FADE_IN_TIME)

    def to_main_menu(self):
        self.state = MAIN_MENU

    def end(self):
        self.state = GAME_FADE_OUT
        self.fade_out_timer.start(END_FADE_IN_TIME)

        # gets the end image
        if sum(self.character.items.values()) < 2:
            self.end_image = load_image("endings/missing_lots_death.png", return_rect=False)
        elif self.character.has_no_items("filled_water_skin"):
            self.end_image = load_image("endings/thirst_death.png", return_rect=False)
        elif self.character.has_no_items("ugly_green_scarf"):
            self.end_image = load_image("endings/cold_death.png", return_rect=False)
        elif self.character.has_no_items("bread", "cheese", "jerky"):
            self.end_image = load_image("endings/starvation_death.png", return_rect=False)
        elif self.character.has_no_items("bandages", "bow_arrow", "cheese"):
            self.end_image = load_image("endings/bandits_death.png", return_rect=False)
        elif self.character.has_no_items("pileogold"):
            self.end_image = load_image("endings/no_money_death.png", return_rect=False)
        else:
            # success?
            pass

        self.end_image = pygame.transform.scale(self.end_image, SCREEN_SIZE)

        if DEBUG:
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

