"""Main modul for balls motion simulation."""
from turtle import Screen
from time import sleep
from random import random, randint

from Lesson_14.balls.classes.ball import Ball


def make_screen():
    """Make screen for program."""
    window_width = 900
    window_height = 600
    window = Screen()
    window.bgcolor('white')
    window.title('Simulation motion of balls.')
    window.setup(window_width, window_height)
    window.onkey(window.bye, 'Escape')
    window.tracer(0)
    window.listen()
    return window


def make_balls():
    """Make balls for play."""
    size_ball = (1, 1)
    quantity_balls = 20
    balls = [Ball(size_ball,
                  (random(), random(), random()),
                  randint(1, 7),
                  randint(1, 7))
             for _ in range(quantity_balls)]
    return balls


def main_loop(balls):
    """Main loop controller."""
    step = 0
    while True:
        for ball in balls:
            ball.check_window_limit(screen)
            if step > 40:
                ball.check_collision_ball(balls)
            ball.move()
        step += 1

        screen.update()
        sleep(0.03)


if __name__ == '__main__':
    screen = make_screen()
    kit_balls = make_balls()
    main_loop(kit_balls)
