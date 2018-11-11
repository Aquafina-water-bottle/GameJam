import pygame

from sprites import Sprite
from general import load_image, get_relative, Coords
from constants import *

class Pose:
    def __init__(self):
        # not sure of a good name for this
        # animation_index = 0 or 1 for walking left or right respectively
        self.standing = False

        # -1 = facing left
        # 0 = not facing left or right
        # 1 = facing right
        self.facing_right_left = 0
        self.facing_down = True
        self.animation_index = 0

    @property
    def facing_left(self):
        return self.facing_right_left == -1

    @property
    def facing_not_right_left(self):
        return self.facing_right_left == 0

    @property
    def facing_right(self):
        return self.facing_right_left == 1

    def set_facing_left(self):
        self.facing_right_left = -1

    def set_facing_not_right_left(self):
        self.facing_right_left = 0

    def set_facing_right(self):
        self.facing_right_left = 1

    def increment(self, max_index):
        self.animation_index = (self.animation_index + 1) % max_index

    @property
    def facing_up(self):
        return not self.facing_down

    @facing_up.setter
    def facing_up(self, facing_up):
        self.facing_down = not facing_up

    def __eq__(self, other):
        both_standing = self.standing == other.standing
        both_facing_right_left = self.facing_right_left == other.facing_right_left
        both_facing_down = self.facing_down == other.facing_down

        return both_standing and both_facing_right_left and both_facing_down

    def __repr__(self):
        return "Pose(standing={}, facing_right_left={}, facing_down={})".format(self.standing, self.facing_right_left, self.facing_down)


class PoseImages:
    def __init__(self, *png_names, flip=False):
        self.frames = tuple(load_image(png_name, convert_alpha=True, flip=flip, return_rect=False) for png_name in png_names)

    def __getitem__(self, index):
        return self.frames[index]

class Character(Sprite):
    """
    MC-Back-for-Lup.png
    MC-Back-for-Rup.png
    MC-Back-Lup.png
    MC-Back-Rup.png
    MC-Back.png

    MC-front-for-Lup.png
    MC-front-for-Rup.png
    MC-front-Lup.png
    MC-front-Rup.png
    MC-front.png
    """

    def __init__(self, png_name, x, y):
        super().__init__(png_name, x, y, convert_alpha=True)
        self.weight = 0
        self.points_collected = 0

        self.in_building_entrance = False
        self.in_building_exit = False

        # pose can be (facing):
        #   up, down, up-left, up-right, down-left, down-right
        #   right = down-right, left = up = down-left
        # standing
        self.pose = Pose()

        # prerenders all images
        self.images = {
            "standing-face-down-right": PoseImages("MC-front.png", flip=True),
            "standing-face-up-right": PoseImages("MC-Back.png", flip=True),
            "standing-face-down-left": PoseImages("MC-front.png"),
            "standing-face-up-left": PoseImages("MC-Back.png"),

            "moving-up-right": PoseImages("MC-front-Lup.png", "MC-front-Rup.png", flip=True),
            "moving-up": PoseImages("MC-front-for-Lup.png", "MC-front-for-Rup.png"),
            "moving-up-left": PoseImages("MC-front-Lup.png", "MC-front-Rup.png"),

            "moving-down-right": PoseImages("MC-Back-Lup.png", "MC-Back-Rup.png", flip=True),
            "moving-down": PoseImages("MC-Back-for-Lup.png", "MC-Back-for-Rup.png"),
            "moving-down-left": PoseImages("MC-Back-Lup.png", "MC-Back-Rup.png"),
        }

        # for specific inventory items
        # TODO uncomment when we're using this
        #self.has_water_skin = False
        #self.has_key_a = False
        #self.has_key_b = False

    def update(self, velocity, tick):
        pose = Pose()

        if velocity[Y] > 0:
            pose.facing_down = True
        elif velocity[Y] < 0:
            pose.facing_up = True

        if velocity[X] > 0:
            pose.set_facing_right()
        elif velocity[X] < 0:
            pose.set_facing_left()
        else:
            pose.set_facing_not_right_left()

        if velocity[X] == 0 and velocity[Y] == 0:
            pose.standing = True

        # if changed from not standing to standing, it preserves facing up or down
        if pose.standing and not self.pose.standing:
            self.pose.standing = True
            self.pose.animation_index = 0
            self.update_walk_pose()

        # otherwise, it just replaces the entire pose if they both differ completely
        elif not pose.standing and pose != self.pose:
            self.pose = pose
            self.update_walk_pose()

        # updates the animation tick when moving
        elif not self.pose.standing and tick % RUNNING_ANIMATION_DELAY == 0:
            # checks if the pose is directly moving up and down and not left and right
            if self.pose.facing_not_right_left:
                self.pose.increment(2)
            else:
                self.pose.increment(2)
            self.update_walk_pose()

    def update_walk_pose(self):
        if self.pose.standing:
            if self.pose.facing_up:
                if self.pose.facing_right:
                    image_pose = self.images["standing-face-up-right"]
                else:
                    image_pose = self.images["standing-face-up-left"]
            else:
                if self.pose.facing_right:
                    image_pose = self.images["standing-face-down-right"]
                else:
                    image_pose = self.images["standing-face-down-left"]
        else:
            if self.pose.facing_down:
                if self.pose.facing_left:
                    image_pose = self.images["moving-up-left"]
                elif self.pose.facing_not_right_left:
                    image_pose = self.images["moving-up"]
                else:
                    image_pose = self.images["moving-up-right"]
            else:
                if self.pose.facing_left:
                    image_pose = self.images["moving-down-left"]
                elif self.pose.facing_not_right_left:
                    image_pose = self.images["moving-down"]
                else:
                    image_pose = self.images["moving-down-right"]
        self.image = image_pose[self.pose.animation_index]

    def get_rect_at_feet(self, camera):
        # 4 pixels from main image
        height = (4*SCALE)
        relative_rect = get_relative(self.rect, camera)

        x = relative_rect.x
        y = relative_rect.y + (self.rect.height // 2 - height)
        return pygame.Rect(x, y, self.rect.width, height)

    def get_pixel_at_feet(self, camera):
        # relative_rect = get_relative(self.rect, camera)
        x = camera.x
        y = camera.y + self.rect.height // 2

        return Coords(x, y)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move_back():
        pass

