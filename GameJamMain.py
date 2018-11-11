# import the pygame module, so you can use it
import pygame
import os

from constants import *
from countdown import *
from sprites import *
from building import *


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
        self.points_collected = 0

    def get_relative(self, camera):
        relative_position = self.copy()
        relative_position.x += SCREEN_SIZE[X] // 2 - camera.x
        relative_position.y += SCREEN_SIZE[Y] // 2 - camera.y
        return relative_position

    def move_back(self, camera, other):
        """
        given this rect collides with other_rect, moves back camera to the correct position

        note that y increases as it goes down

        TODO please fix
        """
        print("top", self.top, "other top", other.top, "camera y", camera.y)

        # if the character top is above building bottom, it moves accordingly
        if self.top < other.bottom:
            camera.y += other.bottom - self.top
            print("changed: ", "top", self.top, "other top", other.top, "camera y", camera.y)

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

        self.collectibles = create_collectibles()
        self.buildings = create_buildings()

        # specifies the middle of the screen
        self.character = Character(CHARACTER_MIDDLE, CHARACTER_SIZE)
        # self.character = pygame.Rect(
        #     SCREEN_SIZE[X] // 2 - CHARACTER_SIZE[X] // 2,
        #     SCREEN_SIZE[Y] // 2 - CHARACTER_SIZE[Y] // 2,
        #     60, 60
        # )

        # temporarily transforms the background to the current resolution
        default_background, _ = load_image('sample_background.png')
        self.background = default_background

        self.camera = Coords(*CHARACTER_START)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, background):
        self._background = pygame.transform.scale(background, MAP_SIZE)


    def play(self):
        self.bell.play(6)
        time.sleep(2.2)
        self.bell.play(5)
        while self.running:
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()

            self.clock.tick(60)

    def handle_event(self):
        # event handling, gets all event from the eventqueue
        event = pygame.event.poll()
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            self.running = False

        # checks if the countdown ends
        if get_countdown() <= 0:

            # can do stuff here idk
            self.continue_game = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            self.running = False

    def draw(self):
        color = (255, 100, 0)
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (SCREEN_SIZE[X] // 2 - self.camera.x, SCREEN_SIZE[Y] // 2 - self.camera.y))
        pygame.draw.rect(self.screen, color, self.character)
        # pygame.draw.rect(self.screen, color, pygame.Rect(1000 + self.camera.x, 500 + self.camera.y, 60, 60))
        # pygame.draw.rect(self.screen, color, pygame.Rect(100 + self.camera.x, 100 + self.camera.y, 60, 60))

        # updates all collectibles
        self.collectibles.update(self.character, self.camera)

        # NOTE: TEMPORARY!!!
        for building in self.buildings:
            building._draw(self.screen, self.camera)

        # draws sprites
        self.collectibles.draw(self.screen, self.camera)

        draw_countdown(self.screen, self.font)
        pygame.display.flip()

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.camera.y -= VELOCITY
        if pressed[pygame.K_DOWN]:
            self.camera.y += VELOCITY

        if pressed[pygame.K_LEFT]:
            self.camera.x -= VELOCITY
        if pressed[pygame.K_RIGHT]:
            self.camera.x += VELOCITY

        # checks for the building shit
        for building in self.buildings:
            print("camera:", self.camera, "relative character:", self.character.get_relative(self.camera), "building top:", building.position.top)
            if building.collides(self.character, self.camera):
                # moves back accordingly
                self.character.move_back(self.camera, building.position)

        # gets character position for the next frame

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

