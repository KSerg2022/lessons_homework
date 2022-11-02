"""Make window"""
from turtle import *


class Window:
    """Initialization class Window"""
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 600
    WINDOW_WIDTH_HALB = WINDOW_WIDTH // 2
    WINDOW_HEIGHT_HALB = WINDOW_HEIGHT // 2

    def __init__(self):
        """Initialization window parameters"""
        screen = Screen()
        screen.bgcolor('white')
        screen.setup(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        screen.title('Your game')
        screen.onkey(screen.bye, 'Escape')
        screen.listen()
        screen.tracer(0)
        screen.getshapes()
