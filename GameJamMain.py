# import the pygame module, so you can use it
import pygame
from pygame.locals import K_w, K_s, K_a, K_d
from constants import *
from building import create_buildings



# define a main function
def main():

    # initialize the pygame module
    pygame.init()

    pygame.display.set_caption("Escape The Village")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((500, 500))

    # define a variable to control the main loop
    running = True

    # creates sprites
    # well = Well()
    all_buildings, sprite_group = create_buildings()

    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        event = pygame.event.poll()
        sprite_group.update()
        sprite_group.draw(screen)
        pygame.display.flip()

        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False

        # list_of_keys = pygame.key.get_pressed()
        # temp gets wsad input


class Game:
    def __init__(self):
        self._top_left = START_TOP_LEFT

    @property
    def left(self):
        return self._top_left[0]

    @property
    def top(self):
        return self._top_left[1]



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
