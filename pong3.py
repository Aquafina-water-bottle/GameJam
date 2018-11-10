# create window
# create game
# play game
# close window

import uagame
import pygame, time
from pygame.locals import *

def main():
    global X
    global Y
    X, Y = 0, 1

    window_title = 'Pong'
    window_size = (800, 700)
    window = uagame.Window(window_title, window_size[0],window_size[1])
    window.set_auto_update(False)
    #game = Game(window)
    #game.play()
    Game(window).play()
    window.close()

class Ball:
    """
    An object in this class represents a colored circle.

    :param window: See :py:data:`~Ball.window`
    :param center: See :py:data:`~Ball.center`
    :param velocity: See :py:data:`Ball.velocity`
    :param radius: See :py:data:`~Ball.radius`
    :param color: See :py:data:`~Ball.color`

    :ivar    window: The display window
    :vartype window: uagame.Window

    :ivar    velocity: The velocity (pixels) of the ball
    :vartype velocity: tuple (x, y)

    :ivar    center: The center of the ball
    :vartype center: tuple (x, y)

    :ivar    radius: The radius (pixels) of the ball
    :vartype radius: int

    :ivar    color: The color of the ball
    :vartype color: pygame.Color
    """

    def __init__(self, window, center, velocity, radius, color):
        self.window = window
        self.surface = window.get_surface()
        self.center = list(center)
        self.radius = radius
        self.velocity = list(velocity)
        self.color = pygame.Color(color)

    def draw(self):
        """
        Draws itself on the screen
        """

        pygame.draw.circle(self.surface, self.color, self.center, self.radius)

    def move(self,scoreboard):
        """
        Moves the circle
        """

        for index in (X, Y):
            self.center[index] = (self.center[index] + self.velocity[index])
            if self.center[index] < self.radius:
                self.velocity[index] *= -1
                if index == X:
                    scoreboard[1] += 1
            if self.center[index] + self.radius > self.surface.get_size()[index]:
                self.velocity[index] *= -1
                if index == X:
                    scoreboard[0] += 1

    def collide(self, paddle, location):
        """
        :param paddle: paddles used by the game
        :type  paddle: pygame.Rect

        :param location: the location of the paddle
        :type  location: str keyword as "right" or "left"
        """

        #if location == "right":
            ## the paddle is on the right side
            #if self.velocity[X] > 0 and paddle.collidepoint(self.center):
                #self.velocity[X] *= -1

        #else:
            ## the paddle is on the left side
            #if self.velocity[X] < 0 and paddle.collidepoint(self.center):
                #self.velocity[X] *= -1
        if ((self.velocity[X] > 0 and location == "right") or (self.velocity[X] < 0 and location == "left")) and paddle.collidepoint(self.center):
            self.velocity[X] *= -1

class Game:
    """
    Represents a complete game

    :param window: :py:data:`~Ball.window`

    :ivar    window: The display window
    :vartype window: uagame.Window

    :ivar    max_frames: Specifies how fast the game should run in terms of frames per second
    :vartype max_frames: int

    :ivar    close_clicked: Specifies whether the close button has been pressed or not.
    :vartype close_clicked: bool

    :ivar    continue_game: Specifies whether the game should continue or not.
    :vartype continue_game: bool

    :ivar    ball: Represents the ball in the screen
    :vartype ball: Ball

    :ivar    paddle1: Represents the paddle to the left of the screen
    :vartype paddle1: pygame.Rect

    :ivar    paddle2: Represents the paddle to the right of the screen
    :vartype paddle2: pygame.Rect

    :ivar    scoreboard: Represents the scores of both sides
    :vartype scoreboard: list [left, right]
    """

    def __init__(self, window):
        pygame.key.set_repeat(20, 20)

        self.window = window
        self.max_frames = 60
        self.close_clicked = False
        self.continue_game = True

        # ball options
        ball_center = (window.get_width()//2,window.get_height()//2)
        ball_velocity = (6, 4)
        ball_radius = 10
        ball_color = "white"

        # create ball
        self.ball = Ball(window, ball_center, ball_velocity, ball_radius, ball_color)

        # paddle options
        paddle_size = (20, 130)
        self.paddle_velocity = 10
        self.right_keys = (K_p, K_l)
        self.left_keys = (K_q, K_a)
        self.paddle_color = pygame.Color('white')
        paddle1_coords = (window.get_width()//8 - paddle_size[X], window.get_height()//2 - paddle_size[Y]//2)
        paddle2_coords = (7*(window.get_width()//8) - paddle_size[X], window.get_height()//2 - paddle_size[Y]//2)

        # create paddles
        self.paddle1 = pygame.Rect(paddle1_coords, paddle_size)
        self.paddle2 = pygame.Rect(paddle2_coords, paddle_size)

        # create scoreboard
        self.scoreboard = [0, 0]

        # scoreboards options
        font_size = 80
        font_color = 'white'
        bg_color = 'black'
        self.window.set_font_size(font_size)
        self.window.set_font_color(font_color)
        self.window.set_bg_color(bg_color)


    def play(self):
        """
        Play the game until the player presses the close box.
        """

        pause_time = 1.0 / self.max_frames

        # until player clicks close, the game will play
        while not self.close_clicked:

            # play frame
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()

            # sets the time in velocity
            time.sleep(pause_time)
        self.window.close()
    def handle_event(self):
        """
        Handle each user event by changing the game state appropriately
        """

        #     if (A and Q) or (P and L) are pressed down
        #         return
        #     if A is pressed down
        #         move the left paddle down
        #     if Q is pressed down
        #         move the left paddle up
        #     if L is pressed down
        #         move the right paddle down
        #     if P is pressed down
        #         move the right paddle up
        #     if the top or bottom of any paddle is outside the window
        #         move back in the window
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        # if event.type == KEYDOWN and self.continue_game == True:
        if self.continue_game == True:
            list_of_keys = pygame.key.get_pressed()

            if (list_of_keys[self.right_keys[0]] and list_of_keys[self.right_keys[1]]) == False:
                if list_of_keys[self.right_keys[0]] == True:
                    self.paddle2.move_ip(0, -self.paddle_velocity)

                if list_of_keys[self.right_keys[1]] == True:
                    self.paddle2.move_ip(0, self.paddle_velocity)

            if (list_of_keys[self.left_keys[0]] and list_of_keys[self.left_keys[1]]) == False:
                if list_of_keys[self.left_keys[0]] == True:
                    self.paddle1.move_ip(0, -self.paddle_velocity)

                if list_of_keys[self.left_keys[1]] == True:
                    self.paddle1.move_ip(0, self.paddle_velocity)

            paddles = [self.paddle1, self.paddle2]

            for paddle in paddles:
                if paddle.top < 0:
                    paddle.move_ip(0, -paddle.top)

                if paddle.bottom > self.window.get_height():
                    paddle.move_ip(0, (self.window.get_height()-paddle.bottom))

    def draw(self):
        """
        Draw all game objects
        """
        self.window.clear()
        self.window.draw_string(str(self.scoreboard[0]), 0, 0)
        self.window.draw_string(str(self.scoreboard[1]), self.window.get_width() - self.window.get_string_width(str(self.scoreboard[1])), 0)

        pygame.draw.rect(self.window.get_surface(), self.paddle_color, self.paddle1)
        pygame.draw.rect(self.window.get_surface(), self.paddle_color, self.paddle2)
        self.ball.draw()
        if not self.continue_game:
            pass
        uagame.update()

    def update(self):
        """
        Update the game objects
        """

        self.ball.move(self.scoreboard)
        self.ball.collide(self.paddle1, "left")
        self.ball.collide(self.paddle2, "right")

    def decide_continue(self):
        """
        Check and remember if the game should continue
        """
        if self.scoreboard.count(11) > 0:
            self.continue_game = False

main()
