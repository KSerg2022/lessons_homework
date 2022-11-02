from turtle import Turtle


class Sprite(Turtle):
    """Base sprite"""

    def __init__(self):
        Turtle.__init__(self, shape='circle')
