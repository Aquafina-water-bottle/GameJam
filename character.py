import pygame

from typing import NamedTuple
from sprites import Sprite
from general import load_image
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
            "standing-face-down": PoseImages("MC-front.png"),
            "standing-face-up": PoseImages("MC-Back.png"),

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
                image_pose = self.images["standing-face-up"]
                asdf = "standing-face-up"
            else:
                image_pose = self.images["standing-face-down"]
                asdf = "standing-face-down"
        else:
            if self.pose.facing_down:
                if self.pose.facing_left:
                    image_pose = self.images["moving-up-left"]
                    asdf = "moving-up-left"
                elif self.pose.facing_not_right_left:
                    image_pose = self.images["moving-up"]
                    asdf = "moving-up"
                else:
                    image_pose = self.images["moving-up-right"]
                    asdf = "moving-up-right"
            else:
                if self.pose.facing_left:
                    image_pose = self.images["moving-down-left"]
                    asdf = "moving-down-right"
                elif self.pose.facing_not_right_left:
                    image_pose = self.images["moving-down"]
                    asdf = "moving-down"
                else:
                    image_pose = self.images["moving-down-right"]
                    asdf = "moving-down-right"
        self.image = image_pose[self.pose.animation_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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

