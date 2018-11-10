import pygame
from pygame import KEYUP, K_SPACE, K_RETURN, K_z, K_LSHIFT, K_RSHIFT, K_CAPSLOCK, K_BACKSPACE #@UnresolvedImport
from pygame.locals import *

X, Y = 0, 1

def get_key(key=None):
    """
    Waits until a key is inputted by the event pygame.KEYUP
    
    :param key: Specifies the key required for the code to continue
    :type  key: pygame keyboard constant
    
    :return: The key input
    :rtype:  int
    """
    
    while True:
        # repeats through this if a specific key has to be gotten
        event = pygame.event.poll()
        
        while event.type != KEYUP:
            # does a while loop here until it gets a keyup event
            event = pygame.event.poll()
            
        if (key == None) or (key == event.key):
            return event.key

def convert_color(color):
    """
    Converts the inputted color to a proper pygame.Color object
    
    :param color: Specifies the inputted color
    :type  color: tuple (r, g, b) or color string
    
    :return: The default pygame color
    :rtype: pygame.Color
    
    :raise ValueError: if a color tuple is not a length of 3 or 4
    :raise TypeError: if a color value is not a string or tuple
    """
    
    if isinstance(color, pygame.Color):
        return color
    
    if isinstance(color, str):
        # note that Color(color) turns any string into a rgba format
        return Color(color)
         
    if isinstance(color, tuple):
        if len(color) == 3:
            return Color(color[0], color[1], color[2], 0)
            
        if len(color) == 4:
            return color
            
        # incorrect size
        raise ValueError("Invalid length: must be 3")
        
    # not a proper type
    raise TypeError("Invalid type: Must be a color string or tuple")

def _allign_rect(keyword, window, suppress_exception=False):
    """
    Gets the coords relative to the given window location
    
    :param keyword: 
    :type  keyword: str keyword as topleft, bottomleft, topright, bottomright, midtop, midleft, midbottom, midright, or center
        Converts keyword to coords
    
    :param window: Specifies the display window
    :type  window: unigame.Window
    
    :raise ValueError: if the player inputs an invalid keyword
    
    :returns: the correct position keyword and the coordinates at said position)
    :rtype: tuple (str, str)
    """
    pos_dict = {
        "topleft" : window.surface.get_rect().topleft,
        "midleft" : window.surface.get_rect().midleft,
        "bottomleft" : window.surface.get_rect().bottomleft,
        "topright" : window.surface.get_rect().topright,
        "midright" : window.surface.get_rect().midright,
        "bottomright" : window.surface.get_rect().bottomright,
        "midtop" : window.surface.get_rect().midtop,
        "center" : window.surface.get_rect().center,
        "midbottom" : window.surface.get_rect().midbottom
        }
    
    if keyword in pos_dict:
        # returns the string and the actual coordinates
        return (keyword, pos_dict[keyword])
        
    # defaults to top left only if suppress_exception is set to true
    if (suppress_warning):
        return ("topleft", pos_dict["topleft"])
    
    # raise error without suppress_exception being true
    raise ValueError("Invalid keyword for alligning a rect")

class SetterProperty(object):
    """
    
    """
    
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__
    def __set__(self, obj, value):
        return self.func(obj, value)

class Window:
    """
    Class for general manipulation of the game window
    
    :param window_title: Header at the top of the window
    :type  window_title: str
    
    :param window_size: The size of the window
    :type  window_size: tuple (x, y)
    
    :ivar    ~Window.bg_color: Specifies the background color of the window
    :vartype ~Window.bg_color: tuple (r, g, b) or color string
    
    :ivar    surface: Specifies the window display
    :vartype surface: pygame.Surface
    
    :ivar    height: Specifies the height of the window (Note: it cannot be set to anything)
    :vartype height: int
    
    :ivar    width: Specifies the width of the window (Note: it cannot be set to anything)
    :vartype width: int
    
    :ivar    ~Window.size: Specifies the window size (Note: it cannot be set to anything)
    :vartype ~Window.size: tuple (x, y)
    
    
    :ivar    auto_update: Specifies whether the window 
        and connected text objects update or not (defaults to True)
    :vartype auto_update: bool
    
    :raise ValueError: if a color tuple is not a length of 3 or 4
    :raise TypeError: if a color value is not a string or tuple
    """
    
    """
    Private variables
    
    :ivar    _surface: Controls the display window
    :vartype _surface: pygame.Surface
    
    :ivar    _bg_color: Stores the background color of the window
    :vartype _bg_color: pygame.Color in (r, g, b, a)
    
    :ivar    _size: Specifies the window size
    :vartype _size: tuple (x, y)
    """
    
    def __init__(self, window_title, window_size, bg_color="black", auto_update=True):
        # Regular pygame init
        pygame.init() #@UndefinedVariable
        
        # Sets the screen size and title
        self._surface = pygame.display.set_mode((window_size[X], window_size[Y]))
        pygame.display.set_caption(window_title)
        
        self._size = window_size
        
        # this has to be set first because bg_color uses auto_update
        self.auto_update = auto_update
        self.bg_color = bg_color
        update()
        
    @property
    def surface(self):
        """
        :getter: (*pygame.Surface*) Returns the window surface variable
        """
        return self._surface
    
    @property
    def width(self):
        """
        :getter: (*int*) Returns the window width
        """
        return self._size[X]
    
    @property
    def height(self):
        """
        :getter: (*int*) Returns the window 
        """
        return self._size[Y]
    
    @property
    def size(self):
        return self._size
        
    @property
    def bg_color(self):
        """
        :setter: (*tuple (r, g, b)* or *color string*)
            Fills the background with the color and clears all rendered objects on screen
        :getter: (*pygame.Color*) Returns the color in (r, g, b, a) format
        """
        
        return self._bg_color
    
    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = convert_color(color)
        self._surface.fill(self._bg_color)
        # Resets the position of all text objects
        Text._reset_all(self)
        
        if self.auto_update:
            update()
        
    def clear(self):
        """
        Clears the window by filling it with the default background color.
        """
        
        # This technically works even though it looks like complete garbage because
        # it has a setter method which does more than just assigning the variable to itself.
        # I'm so done with python
        self.bg_color = self.bg_color
        
    def close(self):
        """
        Closes the window
        """
        
        pygame.quit() #@UndefinedVariable
        

class Text:
    """
    :param window: Specifies the display window
    :type  window: unigame.Window
    
    :param size: See :py:data:`~Text.size`
    :param color: See :py:data:`~Text.color`
    :param bg_color: See :py:data:`~Text.bg_color`
    :param transparency: See :py:data:`~Text.transparency`
    :param start_corner: See :py:data:`~Text.start_corner`
    :param start_coords: See :py:data:`~Text.start_coords`
    
    :ivar    ~Text.size: Specifies the font size
    :vartype ~Text.size: int

    :ivar    color: Specifies the text color
    :vartype color: tuple (r, g, b) or color string
    
    :ivar    font_height: Specifies the font height (Note: it cannot be set to anything)
    :vartype font_height: int
    
    :ivar    ~Text.bg_color: Specifies the color of the text background
    :vartype ~Text.bg_color: tuple (r, g, b) or color string
    
    :ivar    transparency: Specifies whether the background is transparent or not
    :vartype transparency: bool
    
    :ivar    start_corner: Specifies where the coordinates should be relative to the first text box
    :vartype start_corner: keyword
    
    :ivar    start_coords: Specifies where coordinates of the text box will be
            (if given a keyword, the coordinates will be relative to the window)
    :vartype start_coords: tuple (int x, int y) or keyword
    
    :raise ValueError: if a color tuple is not a length of 3 or 4
    :raise TypeError: if a color value is not a string or tuple
    """
    
    """
    Private variables
    
    :cvar    _text_list: Contains all text objects
    :vartype _text_list: list
    
    :cvar    _pos_dict: Contains the coordinates relative to the window given a keyword
    :vartype _pos_dict: dict
    
    :ivar    _window: Controls the display window
    :vartype _window: unigame.Window
    
    :ivar    _size: Stores the font size
    :vartype _size: int
    
    :ivar    _color: Stores the text color
    :vartype _color: pygame.Color in (r, g, b, a)
    
    :ivar    _bg_color: Stores the color of the text background
    :vartype _bg_color: pygame.Color in (r, g, b, a)
    
    :ivar    _font: Controls general font attributes
    :vartype _font: pygame.font.Font
    
    :ivar    _font_height: Stores the font height
    :vartype _font_height: int
    
    :ivar    _y_increment: Number of y pixels down from the starting position
    :vartype _y_increment: int
    
    :ivar    _start_corner: Stores the initial relative position keyword
    :vartype _start_corner: str
    
    :ivar    _start_coords: Stores the initial position coordinates
    :vartype _start_coords: tuple (int x, int y)
    """
    
    _text_list = []
    
    _pos_dict = {
        "topleft" : self._window.surface.get_rect().topleft,
        "midleft" : self._window.surface.get_rect().midleft,
        "bottomleft" : self._window.surface.get_rect().bottomleft,
        "topright" : self._window.surface.get_rect().topright,
        "midright" : self._window.surface.get_rect().midright,
        "bottomright" : self._window.surface.get_rect().bottomright,
        "midtop" : self._window.surface.get_rect().midtop,
        "center" : self._window.surface.get_rect().center,
        "midbottom" : self._window.surface.get_rect().midbottom
        }
    
    def __init__(self, window, size=24, color="white", bg_color="black", transparency=False, start_corner="topleft", start_coords="topleft"):
        self._window = window
        self.size = size
        """
        :getter: (*int*) Returns the font size 
        :setter: (*int*) Sets the font size
        """
        
        self.color = color
        """
        :getter: (*pygame.Color*) Returns the color in (r, g, b, a) format
        :setter: (*tuple (r, g, b)*) Sets the text color
        :setter: (*color string*) Converts keyword to the proper pygame.Color type and sets the text color
        """
        
        self.bg_color = bg_color
        """
        :getter: (*pygame.Color*) Returns the color in (r, g, b, a) format
        :setter: (*tuple (r, g, b)*) Sets the background color
        :setter: (*color string*) Converts keyword to the proper pygame.Color type and sets the background color
        """
        
        self.transparency = transparency
        """
        Specifies whether the background is transparent or not
        """
        
        self.start_corner = start_corner
        """
        :getter: (*tuple (x, y)*) Returns the coordinates of the initial position
        :setter: (*tuple (x, y)*) Sets the coordinates
        :setter: (*str* keyword as *topleft, bottomleft, topright, bottomright, midtop, midleft, midbottom, midright*, or *center*)
            Converts keyword to coordinates
        """
        
        Text._text_list.append(self)
    
    @property
    def font_height(self):
        """
        :getter: (*int*) Returns the font height
        """
        return self._font_height
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._font = pygame.font.Font(None, size)
        self._font_height = self._font.get_height()
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = convert_color(color) 
    
    @property
    def bg_color(self):
        return self._bg_color
    
    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = convert_color(color) 
    
    @property
    def start_corner(self):
        return self._start_corner
    
    @start_corner.setter
    def start_corner(self, position):
        
        if position in Text._pos_dict:
            # stores the string
            self._start_corner = position
            
        else: # defaults to top left
            # stores the string
            self._start_corner = "topleft"
    
    @property
    def start_coords(self):
        return self._start_coords
    
    @start_coords.setter
    def start_coords(self, position):
        
        if position in Text._pos_dict:            
            # gets the actual coordinates
            self._start_coords_coords = Text._pos_dict[position]
            
        else: # defaults to top left
            # gets the actual coordinates (tuple)
            self._start_coords_coords = Text._pos_dict["topleft"]
            
        # resets y increment
        self._y_increment = 0
    
    @staticmethod
    def _reset_all(window):
        """
        Called when the window is cleared to reset all connected text objects
        
        Resets text placements for all text objects by resetting the y increment
        and resets the background to the window background color
        """
        
        for text in Text._text_list:
            if text._window == window:
                text._y_increment = 0
                text.bg_color = text._window.bg_color
    
    def display(self, *lines, cont=True, coords=None):
        """
        Takes line arguments to be rendered on the screen
        
        :param lines: Lines that will be displayed on the window
        :type  lines: tuple of strings or any number of strings
        
        :param cont: Specifies if the text will be displayed on the next line
        :type  cont: bool
        
        :param coords: Custom coordinates based off of the text position
        :type  coords: tuple (x, y)
        """
        
        if coords != None:
            self.start_coords = coords
            
        for line in lines:
            # if the line is a tuple or list, will iterate through that instead
            if isinstance(line, tuple) or isinstance(line, list):
                for true_line in line:
                    self._render_line(true_line, cont)
            else:
                self._render_line(line, cont)
    
    def input(self, line, cont=True, pos=None):
        """
        Takes a single line argument to be rendered on the screen
        
        :param line: The line that will be displayed on the window
        :type  line: str
        
        :param cont: Specifies if the text will be displayed on the next line
        :type  cont: bool
        
        :param pos: Custom coordinates based off of the text position
        :type  pos: tuple (x, y)
        """
        
        key = ""
        player_input = ""
        
        while key != K_RETURN:
            
            # additional space is beside to remove the previous text render
            # if you use backspace
            self.display("   " + line + player_input + "   ", cont=False, pos=pos)
            key = get_key()
            
            # key_state is a dict with each key mapping to a bool
            key_state = pygame.key.get_pressed()
            
            if (K_SPACE <= key <= K_z):
                if key == K_SPACE:
                    player_input += ' '
                else:
                    if key_state[K_LSHIFT] or key_state[K_RSHIFT] or key_state[K_CAPSLOCK]:
                        # makes letters uppercase
                        # however, ignores special characters (eg. @)
                        player_input += pygame.key.name(key).upper()
                    else:
                        # regular key
                        player_input += pygame.key.name(key)
                
            if key == K_BACKSPACE:
                # removes a letter from the player input
                player_input = player_input[:-1]
                
        # has to manually increment here because self.display constantly is set to cont=False
        if (cont):
            self._y_increment += self.font_height
        return player_input
    
    def _render_line(self, line, cont):
        """
        Actually renders the text
        
        :param line: Text to be rendered on its individual line
        :type  line: str
        
        :param cont: Specifies whether the 
        :type  cont: bool
        """
        
        # converts the line to a string no matter what it is
        rendered_line = str(line)
        
        # True refers to whether the line should have smooth edges or not
        if self.transparency == True:
            text_render = self._font.render(rendered_line, True, self.color)
        else:
            text_render = self._font.render(rendered_line, True, self.color, self.bg_color)
        text_pos = text_render.get_rect()
        
        # determines where the x and y coordinates are relative to the text box
        if self.start_corner == "topleft":
            text_pos.topleft = self.start_coords
            
        elif self.start_corner == "midleft":
            text_pos.midleft = self.start_coords
            
        elif self.start_corner == "bottomleft":
            text_pos.bottomleft = self.start_coords
            
        elif self.start_corner == "midtop":
            text_pos.midtop = self.start_coords
            
        elif self.start_corner == "midbottom":
            text_pos.midbottom = self.start_coords
            
        elif self.start_corner == "center":
            text_pos.center = self.start_coords
            
        elif self.start_corner == "topright":
            text_pos.topright = self.start_coords
            
        elif self.start_corner == "midright":
            text_pos.midright = self.start_coords
            
        elif self.start_corner == "bottomright":
            text_pos.bottomright = self.start_coords
        
        text_pos.y += self._y_increment
        
        # if the text continues, it increases the y increment
        if (cont):
            self._y_increment += self.font_height
        
        self._window.surface.blit(text_render, text_pos)
        
        if self._window.auto_update:
            update()
            
class TextGroup:
    """
    Represents a group of unigame.Text objects
    
    :param text_objects: Any number of text objects
    :type  text_objects: unigame.Text
    
    :ivar    group: Holds all of the given text objects
    :vartype group: list of unigame.Text objects
    """
    
    def __init__(self, *text_objects):
        self.group = []
        for text in text_objects:
            self.group.append(text)
    
    def __add__(self, text):
        """
        Adds the given text object to the group
        
        :param text: A text object
        :type  text: unigame.Text
        """
        self.group.append(text)
    
    def __len__(self):
        """
        Returns the length of the group of text objects
        """
        
        return len(self.group)
    
    @SetterProperty
    def size(self, size):
        """
        Sets the size of all of the text objects to the given size
        
        :param size: see ~Text.size
        """
        
        for text in self.group:
            text.size = size
    
    @SetterProperty
    def color(self, color):
        """
        Sets the color of all of the text objects to the given color
        
        :param color: see ~Text.color
        """
        
        for text in self.group:
            text.color = color
    
    @SetterProperty
    def bg_color(self, bg_color):
        """
        Sets the bg_color of all of the text objects to the given bg_color
        
        :param bg_color: see ~Text.bg_color
        """
        
        for text in self.group:
            text.bg_color = bg_color
    
    @SetterProperty
    def start_pos(self, start_pos):
        """
        Sets the start_pos of all of the text objects to the given start_pos
        
        :param start_pos: see ~Text.start_pos
        """
        
        for text in self.group:
            text.start_pos = start_pos
    
    def add(self, *text_objects):
        """
        Adds the given number of text objects into the group
        
        :param text_objects: Any number of text objects
        :type  text_objects: unigame.Text
        
        """
        
        for text in text_objects:
            self.group.append(text)
            
class Velocity:
    """
    General class to add velocity to a sprite in terms of
    cartesian (x, y) or polar coordinates (radius, radians).
    
    :ivar    edge_action: Specifies whether the sprite bounces or wraps around the edge
    :vartype edge_action: keyword "wrap", "bounce" or None
    
    :ivar    sprites: Specifies the sprite provided to move
    :vartype sprites: pygame.sprite.Sprite
     
    :ivar    cartesian: Specifies the cartesian velocity in the x and y directions
    :vartype cartesian: float tuple (x, y)
    
    :ivar    polar: Specifies the polar velocity in the x and y directions
    :vartype polar: float tuple (radius, radians)
    
    :ivar    velocity: Specifies the velocity with your set velocity type (polar or cartesian)
    :vartype velocity: float tuple (x, y) or (radius, radians)
    
    :ivar    type: Specifies the velocity and acceleration type
    :vartype type: str "polar" or "cartesian"
    """
    
    def __init__(self, sprite, velocity=(0, 0), acceleration=(0, 0), edge_action=None):
        pass
    
    @classmethod
    def from_cartesian(self, sprite, velocity=(0, 0), acceleration=(0, 0), edge_action=None):
        pass
    
    @property
    def velocity(self):
        return self._velocity
    
    @property
    def cartesian(self):
        pass
    
    @cartesian.setter
    def cartesian(self):
        pass
    
    @property
    def polar(self):
        pass
    
    @polar.setter
    def polar(self):
        pass
    
    @property
    def next(self):
        """
        :return: The next pair of coordinates
        :rtype:  float tuple (x, y)
        """
        pass
    
    @staticmethod
    def to_polar(vector):
        """
        Converts the input vector to a polar vector
        
        :param vector: 
        :type  vector: float tuple (x, y)
        
        :return:  
        :rtype: float tuple (radius, theta (rad)) 
        """
        pass
    
    @staticmethod
    def to_cartesian(vector):
        """Converts the input vector to a cartesian vector"""
        pass
    
    def to_polar(self):
        """
        Changes both its acceleration and velocity vector to polar vectors
        
        Note that it doesn't change anything if the type is already polar
        """
        pass
    
    def to_cartesian(self):
        """
        Changes both its acceleration and velocity vector to polar vectors
        
        Note that it doesn't change anything if the type is already cartesian
        """
        pass
    
class Image:
    """
    Simply makes a surface object to be used with the attribute self.image
    for a user defined pygame.sprite.Sprite class. It provides a template for
    circles, rectangles, and polygons.
    
    GOAL- Create surface with a given shape using the pygame.draw method
        -Make sure the background is actually transparent
    That surface can be used with the actual creation of a sprite (with self.image) to do literally whatever with
    
    Note:
    - Rect records the hitbox and the position of the object. It is *never drawn*
    - Image represents the displayed sprite image
    """
    
    @staticmethod
    def _get_size(size, using_radius=False):
        if isinstance(size, pygame.Rect):
            return (size.width, size.height)
        
        if isinstance(size, tuple):
            if len(size) == 2:
                return (size[X], size[Y])
        
            # incorrect size
            raise ValueError("Invalid length: must be 2")
        
        if (using_radius):
            if isinstance(size, int) or isinstance(size, float):
                return (size, size)
            
            # not a proper type but can use radius
            print(type(size))
            raise TypeError("Invalid type: Must be a pygame.Rect object, tuple or number")
        else:
            # not a proper type
            raise TypeError("Invalid type: Must be a pygame.Rect object or tuple")

    @staticmethod
    def from_image(window, image_path, start_pos=(0, 0), get_rect=True):
        """
        :param image: Path to the image file
        :type  image: str
        """
        
        image = None
        return image
    
    @staticmethod
    def from_rect(window, size, start_pos=(0, 0), color="white", width=0, get_rect=True):
        """
        :param size: Represents the size of the rectangle
        :type  size: tuple (width, height) or pygame.Rect
        """
        
        image = None
        return image
    
    @staticmethod
    def from_ellipse(window, size, start_pos=(0, 0), color="white", relative_pos="topleft", width=0, get_rect=True):
        """
        :param window: 
        :type  window: 
        
        :param size: Represents the size of the ellipse
        :type  size: int (radius), tuple (width, height) or pygame.Rect
        
        :param color: 
        :type  color: 
        
        :param start_pos: 
        :type  start_pos: 
        
        :param relative_pos: 
        :type  relative_pos: 
        
        :param width: 
        :type  width: 
        """
        
        # gets the proper size
        size = Image._get_size(size, using_radius=True)
        image = pygame.Surface(size)
        
        # creates a transparent background of white
        image.fill((0,0,0,0))
        image.set_colorkey((0,0,0,0))
        
        
        keyword, pos = _allign_rect(relative_pos, window)
        rect = image.get_rect()
        pygame.draw.ellipse(image, convert_color(color), rect, width)
        rect.x = start_pos[X]
        rect.y = start_pos[Y]
        window.surface.blit(image, rect)
        
        # Uses the ternary operator: (does if true) if (condition) else (does if false)
        return (image, rect) if (get_rect == True) else (image)
    
    @staticmethod
    def from_polygon(window, size, points, start_pos=(0, 0), color="white", width=0, get_rect=True):
        """
        :param size: Represents the size of the ellipse
        :type  size: tuple (width, height) or pygame.Rect
        
        :param points: 
        :type  points: int
        """
        
        image = None
        return image
    
def update():
    """
    Updates the entire window surface
    """
    pygame.display.flip()
        
def _test(sleep_time):
    """
    Private function to test out the features of this module
    """
    
    from time import sleep
    window = Window("ayylmao", (500, 500))
    
    sleep(sleep_time)
    print("green")
    window.bg_color = "green"
     
    sleep(sleep_time)
    print("display text")
    text = Text(window, start_pos="topright")
    text.display("ayylmao")
    text.display("line2")
    # update()
     
    sleep(sleep_time)
    print("yellow")    
    window.bg_color = (255, 255, 0)
    text.bg_color = window.bg_color
     
    sleep(sleep_time)
    print("display text")
    text.size = 50
    text.display("should be reset")
    text.size = 18
    text.display("different font size")
    text.size = 100
    text.display("really big")
     
    sleep(sleep_time)
    print("change text position")
    text.start_pos = "center"
    text.size = 18
    text.display("oh daum")
     
    sleep(sleep_time)
    print("reset text")
    window.clear()
    text.display("clear window", 3)
    text.display("third line")
     
    sleep(sleep_time)
    print("different coordinates")
    text.display("diff. coords", pos=(80, 50))
    text.display("second line")
    text.display("changed to mid right", pos="midright")
     
    sleep(sleep_time)
    print("testing seperate lines")
    text.display("seperate", "lines")
     
    sleep(sleep_time)
    print("clearing the screen and using a tuple")
    text.size = 24
    window.bg_color = "black"
    text.color = "white"
    text.start_corner = "midtop"
    instructions = ("these are", "reallly good", "instructions")
    text.display(instructions)
    text.display("note the yellow background")
     
    text.display("this should the proper bg color")
     
    sleep(sleep_time)
    print(Text._text_list)
    asdf = text.input("Yo does this work ", pos=(300, 200))
    text.display(asdf)
     
    text.display("Press enter")
    get_key(K_RETURN)
    text.display("You have pressed enter")
     
    sleep(sleep_time)
    text.display("The following requires an update", pos="midleft")
    window.auto_update = False
    text.display("Does", "this", "display?")
     
    sleep(sleep_time)
    print("update")
    update()
    
    sleep(sleep_time)
    window.auto_update = True
    text.display("12345", pos="topleft")

    get_key(K_RETURN)
    
    text.bg_color = (0, 0, 0, 0)
    text.display("abcd", pos="topleft")
    get_key(K_RETURN)
    
    text.bg_color = (0, 0, 0, 255)
    text.display("123", pos="topleft")
    get_key(K_RETURN)
    
    text.bg_color = (0, 0, 0, 0)
    text.display("ab", pos="topleft")
    get_key(K_RETURN)
    
    sleep(sleep_time)
    window.close()
    
    sleep(sleep_time)
    
_test(1)
