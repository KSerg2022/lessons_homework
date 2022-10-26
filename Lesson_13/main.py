"""Solar system."""
from turtle import *
from math import *
from random import randint, triangular, choice
from time import sleep


class Planet(Turtle):
    """Determine the model of a planet, an asteroid in the solar system."""

    def __init__(self, planet_size, planet_color, radius, star, increase_angle, name='star'):
        Turtle.__init__(self, shape='circle')
        self.name = name
        self.speed(0)
        self.shapesize(*planet_size)
        self.x = 0
        self.y = 0
        self.color(planet_color)
        self.up()
        self.angle = 0
        self.increase_angle = increase_angle
        self.radius = radius
        self.star = star

    def move(self, x_line=1.0):
        """Simulates orbital movement."""
        self.x = self.radius * cos(self.angle) * x_line
        self.y = self.radius * sin(self.angle)
        self.goto(self.star.xcor() + self.x, self.star.ycor() + self.y)
        self.angle += self.increase_angle


def make_window():
    """Make screen for solar system."""
    screen_width = 0.99
    screen_height = 0.93
    window = Screen()
    window.bgcolor('#04061C')
    window.title('Solar system')
    window.setup(screen_width, screen_height, startx=4, starty=4)
    window.onkey(window.bye, 'Escape')
    window.tracer(0)
    window.listen()
    return window


def make_sun():
    """Make sun."""
    main_star = Turtle(shape='circle')
    main_star.color('#FF7A00')
    main_star.shapesize(5, 5)
    return main_star


def make_planets():
    """Make planets."""
    mercury = Planet((0.4, 0.4), '#6A706E', 150 * 0.46, sun, 0.01 / 0.5)

    venus = Planet((0.95, 0.95), "#CEC191", 150 * 0.7, sun, 0.01 / 0.62)

    earth = Planet((1, 1), 'blue', 150, sun, 0.01)
    luna = Planet((0.3, 0.3), 'gray', 22, earth, 0.05)

    mars = Planet((0.53, 0.53), 'red', 150 * 1.4, sun, 0.01 / 1.88)
    phobos = Planet((0.35, 0.35), 'orange', 20, mars, 0.04)
    deimos = Planet((0.25, 0.25), 'white', 29, mars, 0.03)

    jupiter = Planet((3, 3), '#BB8B43', 150 * 1.8, sun, 0.01 / 4)

    saturn_ring_out = Planet((3.9, 4.4), '#E7C490', 150 * 2.25, sun, 0.01 / 5)
    saturn_ring_in = Planet((3.2, 3.7), '#04061C', 150 * 2.25, sun, 0.01 / 5)
    saturn = Planet((2.5, 2.5), '#FEFFD0', 150 * 2.25, sun, 0.01 / 5)

    uranus = Planet((1.8, 1.8), '#16C1F8', 150 * 2.7, sun, 0.01 / 6)

    return [mercury, venus, earth, mars, jupiter, saturn_ring_out, saturn_ring_in, saturn,
            uranus], [luna, phobos, deimos]


def get_asteroids(quantity: int, star: Turtle) -> list[Planet]:
    """Create a given number of meteorites around a given star."""
    asteroids_color = ['#FFFFFF', 'gray', '#DAE2DB', '#BCBFC8', '#AAA995']
    asteroids = []
    for _ in range(quantity):
        meteor = Planet((0.07, 0.07), choice(asteroids_color), randint(450, 520), star, triangular(0.0008, 0.008))
        asteroids.append(meteor)
    return asteroids


def main():
    """Main loop controller."""
    while True:
        planet_x_line = 2
        satellite_x_line = 1.2
        for planet in planets:
            planet.move(planet_x_line)
        for satellite in satellites:
            satellite.move(satellite_x_line)

        asteroid_x_line = 2
        for asteroid in sun_system_asteroids:
            asteroid.move(asteroid_x_line)

        screen.update()
        sleep(0.01)


if __name__ == '__main__':
    screen = make_window()
    sun = make_sun()
    planets, satellites = make_planets()
    sun_system_asteroids = get_asteroids(500, sun)
    main()
