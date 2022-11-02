"""Modul obstacle"""
from turtle import *
from random import random, randint


class Block(Turtle):
    """Initialization class Block"""

    def __init__(self):
        """Initialization block parameters"""
        super().__init__()
        self.hideturtle()
        self.shape("square")
        self.shapesize(0.75, 2)
        self.up()
        self.color(self.get_color())
        self.window_width_halb = self.screen.window_width() // 2
        self.window_height_halb = self.screen.window_height() // 2
        self.x = self.window_width_halb + 20
        self.y = self.get_position()
        self.goto(self.x, self.y)
        self.showturtle()

    def move_block(self, delta_x):
        """Move blocks"""
        self.goto(self.xcor() - delta_x, self.y)

    def get_position(self):
        """Choose position for block on 'y' axes"""
        return randint(-(self.window_height_halb - 40), self.window_height_halb - 40)

    @staticmethod
    def get_color():
        """Create color in RGB standard (1, 1, 1)"""
        return random(), random(), random()
