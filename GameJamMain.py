# import the pygame module, so you can use it
import pygame
import os

from constants import *
from countdown import *
from sprites import *

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
        return f"Coords(x={self.x}, y={self.y})"

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

        self.clock = pygame.time.Clock()

        self.collectibles = self.create_collectibles()

        # specifies the top left corner of the character
        self.character = pygame.Rect(
            SCREEN_SIZE[X] // 2 - CHARACTER_SIZE[X] // 2,
            SCREEN_SIZE[Y] // 2 - CHARACTER_SIZE[Y] // 2,
            60, 60
        )

        # temporarily transforms the background to the current resolution
        self.background = pygame.image.load(os.path.join('background-1.png'))
        self.background = pygame.transform.scale(self.background, MAP_SIZE)

        self.camera = Coords(self.character.x, self.character.y)

    def create_collectibles(self):
        well = Collectible("well_bottom.png", 50, 100, 5)

        sprite_dict = {
            "well": well,
        }

        group = SpriteGroup(sprite_dict)
        return group

    def play(self):
        while self.running:
            # play frame
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()

            # sets the time in velocity
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
        self.screen.blit(self.background, (self.camera.x, self.camera.y))
        pygame.draw.rect(self.screen, color, self.character)
        pygame.draw.rect(self.screen, color, pygame.Rect(1000 + self.camera.x, 500 + self.camera.y, 60, 60))

        # updates all collectibles
        self.collectibles.update(self.character, self.camera)

        # draws sprites
        self.collectibles.draw(self.screen, self.camera)

        draw_countdown(self.screen, self.font)
        pygame.display.flip()

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.camera.y += 6
        if pressed[pygame.K_DOWN]:
            self.camera.y -= 6

        if pressed[pygame.K_LEFT]:
            self.camera.x += 6
        if pressed[pygame.K_RIGHT]:
            self.camera.x -= 6

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

