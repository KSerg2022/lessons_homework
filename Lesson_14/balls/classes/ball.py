"""Base class ball"""
from random import choice

from Lesson_14.balls.classes.sprite import Sprite


class Ball(Sprite):
    """Ball class."""

    def __init__(self, size_ball, color_ball, increase_position_x, increase_position_y, name='ball'):
        Sprite.__init__(self)
        self.name = name
        self.up()
        self.speed(0)
        self.x = 0
        self.y = 0
        self.shapesize(*size_ball)
        self.color(color_ball)
        self.increase_position_x = increase_position_x
        self.increase_position_y = increase_position_y
        self.direction_x = choice([-1, 1])
        self.direction_y = choice([-1, 1])

    def move(self):
        """Simulates the movement of a ball."""
        self.x = self.x - self.increase_position_x * self.direction_x
        self.y = self.y - self.increase_position_y * self.direction_y
        self.goto(self.x, self.y)


    def check_window_limit(self, screen):
        """Changing the direction of the ball when it collides with the edge of the window."""
        window_width_halb = screen.window_width() / 2
        window_height_halb = screen.window_height() / 2
        right_border = window_width_halb - 20
        left_border = -(window_width_halb - 20)
        top = window_height_halb - 20
        bottom = -(window_height_halb - 20)
        if self.x >= right_border:
            self.x = right_border
            self.direction_x = -self.direction_x
        if self.x <= left_border:
            self.x = left_border
            self.direction_x = -self.direction_x
        if self.y >= top:
            self.y = top
            self.direction_y = -self.direction_y
        if self.y <= bottom:
            self.y = bottom
            self.direction_y = -self.direction_y

    def check_collision_ball(self, balls):
        """Changing the direction of the ball when colliding with another ball."""
        for ball in balls:
            if self.x == ball.x and self.y == ball.y:
                continue
            elif self.distance(ball.x, ball.y) <= 21:
                self.direction_x, ball.direction_x = ball.direction_x, self.direction_x
                self.direction_y, ball.direction_y = ball.direction_y, self.direction_y
