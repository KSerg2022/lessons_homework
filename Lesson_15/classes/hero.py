"""Modul hero"""
from turtle import *
from pathlib import Path
import os


class Hero(Turtle):
    """Initialization class Hero"""
    PATH_TO_IMAGE = str(Path(__name__).parent.absolute())
    PATH_TO_GIF = os.path.join(PATH_TO_IMAGE, 'image', 'tortoise_50.gif')

    def __init__(self):
        """Initialization hero parameters"""
        super().__init__()
        self.screen.register_shape(self.PATH_TO_GIF)
        self.shape(self.PATH_TO_GIF)
        self.up()
        self.hideturtle()
        self.left(90)
        self.x = 0
        self.y = 0
        self.window_height_halb = self.screen.window_height() // 2
        self.y_start = -(self.window_height_halb - 10)
        self.goto(self.x, self.y_start)
        self.showturtle()
        self.delta_y = 3
        self.screen.onkeypress(self.move_hero_up, 'Up')
        self.screen.onkeypress(self.move_hero_down, 'Down')

    def move_hero_up(self):
        """Move hero up"""
        self.goto(self.x, self.ycor() + self.delta_y)

    def move_hero_down(self):
        """Move hero down"""
        self.goto(self.x, self.ycor() - self.delta_y)

    def reset_position(self):
        """Place hero to start position"""
        self.goto(self.x, self.y_start)

    def collision_with_block(self):
        """Stops the hero upon hitting a block"""
        self.delta_y = 0

    def increase_speed_hero(self):
        """Increases the speed of the hero when passing the level"""
        self.delta_y += 1
