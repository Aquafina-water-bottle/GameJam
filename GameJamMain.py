# import the pygame module, so you can use it
import os
import time

import pygame

from constants import *
from countdown import *
from sprites import *
from building import *

begin_time = time.time()

"""
TODO (programming):

- building mechanics:
    - enter buildings:
        - change background
        - load in collectibles
        - ability to exit building

- collectible mechanics:
    - increment points to whatever

- math for collectibles
"""

def main():
    game = Game()
    game.play()

class Coords:
    """
    Temporary class to store coordinates

    Should replace this with some character class or rect object or something lmao
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def copy(self):
        return Coords(self.x, self.y)

    def __repr__(self):
        return "Coords(x={}, y={})".format(self.x, self.y)

class Character(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weight = 0
        self.points_collected = 0

        # for specific inventory items
        # TODO uncomment when we're using this
        #self.has_water_skin = False
        #self.has_key_a = False
        #self.has_key_b = False


    def move_back(self, camera, other, velocity):
        """
        given this rect collides with other_rect, moves back camera to the correct position

        note that y increases as it goes down

        velocity = tuple of (+/-1, +/-1) to determine which way it's moving
        """
        # TODO DOESN'T WORK REEE
        # IDEA: make rect objects of 1 pixel length to represent the top areas and move back accordingly
        # however, how to do masking then?


        camera_bottom = camera.y + CHARACTER_SIZE[Y] // 2
        camera_top = camera.y - CHARACTER_SIZE[Y] // 2
        camera_right = camera.x + CHARACTER_SIZE[Y] // 2
        camera_left = camera.x - CHARACTER_SIZE[Y] // 2

        # when the camera is below the top and it's trying to move down: moves back up
        if velocity[Y] == 1 and other.top < camera_bottom:
            camera.y -= camera_bottom - other.top

        # when the camera is above the bottom and it's trying to move up: moves back down
        if velocity[Y] == -1 and other.bottom > camera_top:
            camera.y += other.bottom - camera_top

        # when the camera is trying to move to the right: moves back left
        # (camera is to the right of the left part of other)
        # if velocity[X] == 1 and other.left < camera_right:
        #     print("moving right")
        #     camera.x -= camera_right - other.left


class Game:
    def __init__(self):
        # initialize the pygame module
        pygame.init()
        self.font = pygame.font.Font(None, 100)
        pygame.display.set_caption("Escape The Village")

        # create a surface on screen that has the size of 240 x 180
        # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        # define a variable to control the main loop
        self.running = True
        self.continue_game = True
        self.bell = pygame.mixer.Sound("assets/churchbell.wav")
        self.clock = pygame.time.Clock()
        self.countdown = Countdown()

        self.collectibles = create_collectibles()
        self.buildings = create_buildings()

        # specifies the middle of the screen
        self.character = Character(CHARACTER_MIDDLE, CHARACTER_SIZE)

        # TODO remove to add fade in
        #self.fade_in = True
        self.fade_in = False; self.countdown.start()  # because annoying

        self.clicked_f = False
        self.holding_f = False

        # temporarily transforms the background to the current resolution
        default_background, _ = load_image('background_outline.png')
        self.background = default_background


        # variables for when you're in some building
        self.in_building = False
        self.current_building = None

        self.camera = Coords(*CHARACTER_START)


    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, background):
        self._background = pygame.transform.scale(background, MAP_SIZE)


    def play(self):
        self.bell.play(6)
        self.bell.play(5)
        while self.running:
            self.handle_event()
            self.draw()
            if self.continue_game and not self.fade_in:
                self.update()

            self.clock.tick(60)

    def handle_event(self):
        # checks if fading has ended
        if self.fade_in and time.time() - begin_time > FADE_IN_TIME:
            self.fade_in = False
            self.countdown.start()

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

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            self.running = False

        # so that F can be pressed once and not held down
        # since when it's held down, clicked_f is set to false
        if pressed[pygame.K_f]:
            if not self.holding_f:
                self.holding_f = True
                self.clicked_f = True
            else:
                self.clicked_f = False
        else:
            self.holding_f = self.clicked_f = False

        print(self.holding_f, self.clicked_f)

    def draw(self):
        color = (255, 100, 0)
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (SCREEN_SIZE[X] // 2 - self.camera.x, SCREEN_SIZE[Y] // 2 - self.camera.y))
        pygame.draw.rect(self.screen, color, self.character)

        # updates all collectibles only when "F" is pressed
        if self.clicked_f:
            self.collectibles.update(self.character, self.camera)

        # NOTE: TEMPORARY!!!
        for building in self.buildings:
            building._draw(self.screen, self.camera)

        # draws sprites
        self.collectibles.draw(self.screen, self.camera)

        self.countdown.draw(self.screen, self.font, self.fade_in)

        if self.fade_in:
            alpha_value = int(255 - 255 * (time.time() - begin_time) / FADE_IN_TIME)
            black_fade_surface = self.screen.copy()
            black_fade_surface.fill(pygame.Color("black"))
            black_fade_surface.set_alpha(alpha_value)

            self.screen.blit(black_fade_surface, (0, 0))

        pygame.display.flip()


    def update(self):
        pressed = pygame.key.get_pressed()
        velocity = [0, 0]
        if pressed[pygame.K_UP]:
            self.camera.y -= VELOCITY
            velocity[Y] -= 1
        if pressed[pygame.K_DOWN]:
            self.camera.y += VELOCITY
            velocity[Y] += 1

        if pressed[pygame.K_LEFT]:
            self.camera.x -= VELOCITY
            velocity[X] -= 1
        if pressed[pygame.K_RIGHT]:
            self.camera.x += VELOCITY
            velocity[X] += 1

        if not self.in_building:
            # checks for the building shit
            for building in self.buildings:
                pass
                # if building.enters(self.character, self.camera):
                #     print("colliding with entrance")
                # else:
                #     print()
                # TODO doesn't actually work lmao
            #     if building.collides(self.character, self.camera):
            #         # moves back accordingly
            #         self.character.move_back(self.camera, building.position, tuple(velocity))

        else:
            # checks 
            pass


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

