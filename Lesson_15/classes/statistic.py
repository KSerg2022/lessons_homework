"""Modul statistic data"""
from turtle import Turtle


class Statistic(Turtle):
    """Initialization class Statistic"""

    def __init__(self):
        """Initialization statistic parameters"""
        super().__init__()
        self.pu()
        self.level = 1
        self.txt = 'Level: '
        self.hideturtle()

    def level_up(self):
        """Increase game level"""
        self.reset()
        self.up()
        self.hideturtle()
        self.level += 1
        return self.level

    def print_level(self):
        """Print massage with level's game"""
        self.goto(-445, 268)
        self.color('orange')
        style = ("Verdana", 20, "normal")
        return self.write(f'{self.txt}{self.level}', move=False, font=style, align="left")

    def print_game_over(self):
        """Print massage that game is over"""
        self.goto(0, 0)
        self.color('cyan')
        style = ('Courier', 30, 'bold')
        return self.write(f'Game over.', move=False, font=style, align="center")
