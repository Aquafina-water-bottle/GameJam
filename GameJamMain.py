import os

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
from scaled_rect import ScaledRect

"""
TODO (programming):
- get jared ssh lmao

- win condition (discuss balancing)
    - math for collectibles
"""

def main():
    game = Game()
    game.play()

class Game:
    def __init__(self):
        # initialize the pygame module
        pygame.init()

        logo_name = os.path.join('assets', "logo.bmp")
        logo  = pygame.image.load(logo_name)
        pygame.display.set_icon(logo)

        pygame.display.set_caption("Escape")
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.black_surface = self.screen.copy()
        self.black_surface.fill(pygame.Color("black"))

        # default font used for the timer
        self.font = pygame.font.Font(None, 100)
        self.subtext_font = pygame.font.Font(None, 25)
        self.notification_font = pygame.font.Font(None, 25)

        # specifies the middle of the screen
        self.character = Character("avatar/MC-front.bmp", 0, 0)
        self.camera = Coords(CHARACTER_START[X], CHARACTER_START[Y])

        # saves the camera for when enering the building
        self.camera_save = None
        self.user_input = UserInput()

        # sound
        self.ambient = pygame.mixer.Sound("assets/ambient.wav")
        self.ambient_channel = pygame.mixer.Channel(1)
        self.wind = pygame.mixer.Sound("assets/wind.wav")
        self.wind.play(-1)

        # a shit ton of time related stuff
        self.clock = pygame.time.Clock()
        self.countdown = Countdown()
        self.ticker = Ticker()
        self.fade_in_timer = Timer()
        self.display_timer = Timer()
        self.notification_timer = Timer()
        self.fade_out_timer = Timer()

        # define a variable to control the main loop
        # where it is really only set to false if the player exits or the X button is pressed
        self.running = True
        self.state = None
        self.fade_into_main_menu()

        # variables for when you're in some building
        self.current_building = None
        self.buildings = create_buildings()
        self.well_area = ScaledRect(208, 354, 60, 51)

        self.wins = create_wins()
        self.subtext_value = ""
        self.notification_value = ""

        # self.ended = False
        # self.show_ending = False

        self.end_image = None
        self.begin_image = load_image("beginlol.bmp", use_scale=False, return_rect=False)
        self.begin_image = pygame.transform.scale(self.begin_image, SCREEN_SIZE)

        self.default_background = load_image('background.bmp', return_rect=False)
        self.building_wall_mask = load_image('background_outline.bmp', convert_alpha=True, return_rect=False)

        # background can change to default background or house background
        self.background = self.default_background

        # creates the start menus
        self.pause_menu = PauseMenu(self.screen)
        self.main_menu = MainMenu(self.screen)

        self.temp = []

    @property
    def in_building(self):
        return self.current_building is not None

    def play(self):
        while self.running:
            if DEBUG:
                print(STATE_DICT[self.state])
            self.handle_event()
            self.update()
            self.draw()

            self.clock.tick(60)

        if DEBUG:
            print("debug: temp =", self.temp)
            print("collected {}".format(self.character.items))

    def handle_event(self):
        self.user_input.update()
        self.ticker.update()

        # can only pause when you're in the fucking game matey lmao
        if self.state == GAME_PLAY and self.user_input.clicked_pause(self.ticker.tick):
            self.pause()
        elif self.state == GAME_PAUSE:
            if self.user_input.clicked_mouse():
                pos = pygame.mouse.get_pos()
                if self.pause_menu.resume_button.border.collidepoint(pos):
                    self.unpause()
                if self.pause_menu.exit_button.border.collidepoint(pos):
                    self.running = False
            if self.user_input.clicked_pause(self.ticker.tick):
                self.unpause()

        # checks for main menu clicks
        if self.state == MAIN_MENU:
            if self.user_input.clicked_mouse():
                pos = pygame.mouse.get_pos()
                if self.main_menu.play_button.border.collidepoint(pos):
                    self.fade_outof_main_menu()
                if self.main_menu.exit_button.border.collidepoint(pos):
                    self.running = False
                    return
            if self.user_input.clicked_interact(self.ticker.tick):
                self.fade_outof_main_menu()

        # only do something if the event is of type QUIT
        if self.user_input.clicked_quit():
            # change the value to False, to exit the main loop
            self.running = False
            return

        # if the player presses interact and it's during one of the display screens
        if self.user_input.clicked_interact(self.ticker.tick):
            if BEGIN_FADE_IN <= self.state <= BEGIN_FADE_OUT:
                self.start_game_fade_in()

            if END_FADE_IN <= self.state <= END_FADE_OUT:
                self.fade_into_main_menu()

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
                if self.state == MAIN_MENU_FADE_IN:
                    # menu fade in to main menu
                    self.to_main_menu()

                elif self.state == BEGIN_FADE_IN:
                    # end instruction fade in
                    self.state = BEGIN_DISPLAY
                    self.display_timer.start(BEGIN_DISPLAY_TIME)

                elif self.state == GAME_FADE_IN:
                    # starts the game here (end fade in)
                    self.countdown.start()
                    self.ambient_channel.play(self.ambient)
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
                    self.fade_into_main_menu()

        # countdown ends: game ends
        if self.state == GAME_PLAY and self.countdown.ended:
            self.end()

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

            if not self.in_building:
                # detects collision with walls and buildings
                pixel = (self.building_wall_mask.get_at(tuple(self.character.get_pixel_at_feet(self.camera))))
                if pixel[3] > ALPHA_THRESHOLD:
                    # TODO make less sticky if possible
                    if COLLIDES:
                        # checks for each x and y if they can work
                        current_x = self.camera.x
                        current_y = self.camera.y

                        self.camera.x = self.camera.previous_x
                        self.camera.y = self.camera.previous_y

                        coords = Coords(current_x, current_y)
                        coords.x = self.camera.previous_x       # gets the new y coordinate and keeps x constant
                        pixel = (self.building_wall_mask.get_at(tuple(self.character.get_pixel_at_feet(coords))))
                        if not (pixel[3] > ALPHA_THRESHOLD):    # if the new y coordinate is free
                            self.camera.y = coords.y

                        coords = Coords(current_x, current_y)
                        coords.y = self.camera.previous_y
                        pixel = (self.building_wall_mask.get_at(tuple(self.character.get_pixel_at_feet(coords))))
                        if not pixel[3] > ALPHA_THRESHOLD:
                            self.camera.x = coords.x

                # checks for collecting water at the well
                if (self.well_area.collide(self.camera, self.character.proper_size) and self.character.items["water_skin"] >= 1):
                    self.subtext_value = "Press {} to fill your water skin".format(INTERACT_KEY)
                    if self.user_input.clicked_interact(self.ticker.tick):
                        self.character.items["water_skin"] -= 1
                        self.character.items["filled_water_skin"] += 1
                        self.notification_value = "Filled your water skin"
                        self.notification_timer.start(NOTIFICATION_TIME)

                # checks for the building shit
                for building in self.buildings:
                    if building.enters(self.character, self.camera):
                        self.subtext_value = "Press {} to enter ".format(INTERACT_KEY) + building.name

                        if self.user_input.clicked_interact(self.ticker.tick):
                            self.notification_value = "Entered " + building.name
                            self.notification_timer.start(NOTIFICATION_TIME)

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
                        # set player to escaped
                        self.character.escaped = True
                        # ambient fades out only here
                        self.ambient_channel.fadeout(AMBIENT_FADE_OUT)
                        self.end()

            else:
                # detects collision with the building walls by checking
                # if the player leaves the given rect
                coords = tuple(self.character.get_pixel_at_feet(self.camera))
                if not self.current_building.walls.rect.collidepoint(coords):
                    # TODO make less sticky if possible

                    if COLLIDES:
                        # checks for each x and y if they can work
                        current_x = self.camera.x
                        current_y = self.camera.y

                        self.camera.x = self.camera.previous_x
                        self.camera.y = self.camera.previous_y

                        coords2 = Coords(current_x, current_y)
                        coords2.x = self.camera.previous_x       # gets the new y coordinate and keeps x constant
                        if self.current_building.walls.rect.collidepoint(tuple(self.character.get_pixel_at_feet(coords2))):
                            self.camera.y = coords2.y

                        coords2 = Coords(current_x, current_y)
                        coords2.y = self.camera.previous_y
                        if self.current_building.walls.rect.collidepoint(tuple(self.character.get_pixel_at_feet(coords2))):
                            self.camera.x = coords2.x

                # detects collision for furniture
                for furniture in self.current_building.furniture.values():
                    if furniture.rect.collidepoint(coords):
                        # TODO make less sticky if possible
                        if COLLIDES:
                            # checks for each x and y if they can work
                            current_x = self.camera.x
                            current_y = self.camera.y

                            self.camera.x = self.camera.previous_x
                            self.camera.y = self.camera.previous_y

                            coords2 = Coords(current_x, current_y)
                            coords2.x = self.camera.previous_x       # gets the new y coordinate and keeps x constant
                            if not furniture.rect.collidepoint(tuple(self.character.get_pixel_at_feet(coords2))):
                                self.camera.y = coords2.y

                            coords2 = Coords(current_x, current_y)
                            coords2.y = self.camera.previous_y
                            if not furniture.rect.collidepoint(tuple(self.character.get_pixel_at_feet(coords2))):
                                self.camera.x = coords2.x


                # checks for collectibles
                for collectible in self.current_building.collectibles:
                    if collectible.collides(self.character, self.camera):
                        self.subtext_value = "Collect " + collectible.display_name

                        if self.user_input.clicked_interact(self.ticker.tick):
                            collectible.pick_up()
                            self.notification_value = "Collected " + collectible.display_name
                            self.notification_timer.start(NOTIFICATION_TIME)
                            self.character.items[collectible.type] += 1
                            #self.character.points += collectible.points
                            #self.character.weight += collectible.weight

                # checks whether they have left the building
                if self.current_building.exit_area.collide(self.camera, self.character.get_rect_at_feet()):
                    self.subtext_value = "Press {} to leave ".format(INTERACT_KEY) + self.current_building.name

                    if self.user_input.clicked_interact(self.ticker.tick):
                        self.notification_value = "Left " + self.current_building.name
                        self.notification_timer.start(NOTIFICATION_TIME)
                        self.camera = self.camera_save
                        self.current_building = None
                        self.background = self.default_background

    def draw(self):
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
                    self.well_area.debug_draw(self.camera, self.screen, "pink")

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

            # renders the display name on the bottom right of the screen
            if self.subtext_value:
                text_render = self.subtext_font.render(self.subtext_value, True, pygame.Color("orange"))
                # text_render = pygame.transform.scale(text_render, (text_render.get_width()*3, text_render.get_height()*3))
                text_pos = text_render.get_rect()
                text_pos.bottomleft = self.screen.get_rect().bottomleft
                self.screen.blit(text_render, text_pos)
                self.subtext_value = ""

            if self.notification_value:
                if self.notification_timer.ended:
                    self.notification_value = ""
                else:
                    text_render = self.notification_font.render(self.notification_value, True, pygame.Color("orange"))
                    # text_render = pygame.transform.scale(text_render, (text_render.get_width()*3, text_render.get_height()*3))
                    text_pos = text_render.get_rect()
                    text_pos.bottomleft = self.screen.get_rect().bottomleft
                    text_pos.y -= 25
                    self.screen.blit(text_render, text_pos)

        # displays the beginning image
        if BEGIN_FADE_IN <= self.state <= BEGIN_FADE_OUT:
            self.screen.blit(self.begin_image, (0, 0))

        # displays the ending image
        if END_FADE_IN <= self.state <= END_FADE_OUT:
            self.screen.blit(self.end_image, (0, 0))

        # displays the main menu
        if self.state in (MAIN_MENU_FADE_IN, MAIN_MENU, MAIN_MENU_FADE_OUT):
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


    def start_game_fade_in(self):
        self.state = GAME_FADE_IN
        self.fade_in_timer.start(GAME_FADE_IN_TIME)

    def pause(self):
        #pygame.mixer.pause()
        self.ambient_channel.pause()
        self.countdown.pause()
        self.state = GAME_PAUSE

    def unpause(self):
        #pygame.mixer.unpause()
        self.ambient_channel.unpause()
        self.countdown.unpause()
        self.state = GAME_PLAY

    def fade_into_main_menu(self):
        # does the majority of resetting here if necessary
        # fades out if there's still sound for some reason
        self.countdown.start()
        self.countdown.pause()
        self.ambient_channel.fadeout(2)
        self.character.reset()
        self.camera = Coords(CHARACTER_START[X], CHARACTER_START[Y])

        self.fade_in_timer.start(MAIN_MENU_FADE_IN_TIME)
        self.state = MAIN_MENU_FADE_IN

    def to_main_menu(self):
        self.state = MAIN_MENU

    def fade_outof_main_menu(self):
        self.state = MAIN_MENU_FADE_OUT
        self.fade_out_timer.start(MAIN_MENU_FADE_OUT_TIME)

    def end(self):
        if not self.countdown.ended:
            self.countdown.pause()
        self.state = GAME_FADE_OUT
        self.fade_out_timer.start(GAME_FADE_OUT_TIME)

        # gets the end image
        if not self.character.escaped:
            self.end_image = load_image("endings/stay_death.bmp", return_rect=False)
        elif sum(self.character.items.values()) <= 2:
            self.end_image = load_image("endings/missing_lots_death.bmp", return_rect=False)
        elif self.character.has_no_items("filled_water_skin"):
            self.end_image = load_image("endings/thirst_death.bmp", return_rect=False)
        elif self.character.has_no_items("ugly_green_scarf"):
            self.end_image = load_image("endings/cold_death.bmp", return_rect=False)
        elif self.character.has_no_items("bread", "cheese", "jerky"):
            self.end_image = load_image("endings/starvation_death.bmp", return_rect=False)
        elif self.character.has_no_items("bandages", "bow_arrow", "cheese"):
            self.end_image = load_image("endings/bandits_death.bmp", return_rect=False)
        elif self.character.has_no_items("pileogold"):
            self.end_image = load_image("endings/no_money_death.bmp", return_rect=False)
        else:
            self.end_image = load_image("endings/win_happy.bmp", return_rect=False)

        self.end_image = pygame.transform.scale(self.end_image, SCREEN_SIZE)

        if DEBUG:
            print("ended!")



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()

