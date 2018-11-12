import pygame

from sprites import Sprite
from general import load_image, scale_rect, get_relative, Coords
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
        self.frames = tuple(load_image("avatar/MC-" + png_name, convert_alpha=True, flip=flip, return_rect=False) for png_name in png_names)

    def __getitem__(self, index):
        return self.frames[index]

class Character(Sprite):
    def __init__(self, png_name, x, y):
        super().__init__(png_name, x, y, convert_alpha=True)
        self.weight = 0
        self.points = 0
        self.items = {
            "bandages": 0,
            "bow_arrow": 0,
            "bread": 0,
            "cheese": 0,
            "daggers": 0,
            "jerky": 0,
            "pileogold": 0,
            "sword": 0,
            "ugly_green_scarf": 0,
            "water_skin": 0,        # empty
            "filled_water_skin": 0,
        }

        self.in_building_entrance = False
        self.in_building_exit = False

        # pose can be (facing):
        #   up, down, up-left, up-right, down-left, down-right
        #   right = down-right, left = up = down-left
        # standing
        self.pose = Pose()

        # prerenders all images
        self.images = {
            "standing-face-down-right": PoseImages("front.png", flip=True),
            "standing-face-up-right": PoseImages("Back.png", flip=True),
            "standing-face-down-left": PoseImages("front.png"),
            "standing-face-up-left": PoseImages("Back.png"),

            "moving-up-right": PoseImages("front-Lup.png", "front-Rup.png", flip=True),
            "moving-up": PoseImages("front-for-Lup.png", "front-for-Rup.png"),
            "moving-up-left": PoseImages("front-Lup.png", "front-Rup.png"),

            "moving-down-right": PoseImages("Back-Lup.png", "Back-Rup.png", flip=True),
            "moving-down": PoseImages("Back-for-Lup.png", "Back-for-Rup.png"),
            "moving-down-left": PoseImages("Back-Lup.png", "Back-Rup.png"),
        }

        # for specific inventory items
        # TODO uncomment when we're using this
        #self.has_water_skin = False
        #self.has_key_a = False
        #self.has_key_b = False

    @property
    def proper_size(self):
        """
        removes 5 pixels from the sides
        """
        x = self.rect.x // SCALE + 6
        y = self.rect.y // SCALE
        width = self.rect.width // SCALE - 6*2
        height = self.rect.height // SCALE
        return scale_rect(pygame.Rect(x, y, width, height))

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
            return False

        # otherwise, it just replaces the entire pose if they both differ completely
        if not pose.standing and pose != self.pose:
            self.pose = pose
            self.update_walk_pose()
            return True

        # updates the animation tick when moving
        if not self.pose.standing and tick % RUNNING_ANIMATION_DELAY == 0:
            # checks if the pose is directly moving up and down and not left and right
            if self.pose.facing_not_right_left:
                self.pose.increment(2)
            else:
                self.pose.increment(2)
            self.update_walk_pose()
            return True
        return False

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

    def get_rect_at_feet(self):
        # 4 pixels from main image

        width = self.rect.width - FEET_WIDTH_REMOVE_SIDES*SCALE*2
        height = (FEET_HEIGHT*SCALE)

        x = self.rect.x + FEET_WIDTH_REMOVE_SIDES*SCALE
        y = self.rect.y + (self.rect.height - height)

        return pygame.Rect(x, y, width, height)

    def get_pixel_at_feet(self, camera):
        # relative_rect = get_relative(self.rect, camera)
        x = camera.x
        y = camera.y + self.rect.height // 2

        return Coords(x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_pixel(self, screen, camera):
        pixel = self.get_pixel_at_feet(camera)
        pixel.x // SCALE * SCALE
        pixel.y // SCALE * SCALE
        rect = pygame.Rect(tuple(pixel), (SCALE, SCALE))
        print(rect)
        pygame.draw.rect(screen, pygame.Color("pink"), get_relative(rect, camera))

    def move_back(self):
        pass
