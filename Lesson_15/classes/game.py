"""Main modul"""
from turtle import *
from time import sleep
from random import randint

from Lesson_15.classes.window import Window
from Lesson_15.classes.block import Block
from Lesson_15.classes.statistic import Statistic
from Lesson_15.classes.hero import Hero


class Game:
    """Initialization class Game"""

    def __init__(self):
        """Initialization game parameter."""
        self.window = Window()
        self.statistic = Statistic()
        self.hero = Hero()
        self.blocks = Block()
        self.block_speed = 1

    def run_game(self):
        """Main controller"""
        blocks_lines = [self.make_blocks()]
        while True:
            self.statistic.print_level()
            self.get_level_up()

            for blocks_line in blocks_lines:
                self.del_empty_blocks_line(blocks_line, blocks_lines)

                for block in blocks_line:
                    block.move_block(self.block_speed)
                    self.check_collision_block_hero(block)
                    self.del_block_outside_window(block, blocks_line)

            self.add_blocks_line(blocks_lines, self.hero.delta_y)
            update()
            sleep(0.001)

    @staticmethod
    def make_blocks():
        """Create blocks line"""
        blocks_line = [Block() for _ in range(randint(0, 4))]
        return blocks_line

    def add_blocks_line(self, blocks_lines, speed_hero):
        """Add blocks line into game"""
        probability_adding_row = 33
        if speed_hero >= 33:
            if randint(0, 1) == 1:
                blocks_lines.append(self.make_blocks())
        else:
            if randint(0, probability_adding_row - speed_hero) == 1:
                blocks_lines.append(self.make_blocks())

    def check_collision_block_hero(self, block):
        """Check collision block with hero"""
        if self.hero.distance(block.xcor(), block.ycor()) < 20:
            self.hero.collision_with_block()
            self.statistic.print_game_over()
            self.stop_block_speed()

    def get_level_up(self):
        """If the hero reaches the top of the window, he gets a level up"""
        if self.hero.ycor() > 290:
            self.hero.reset_position()
            self.hero.increase_speed_hero()
            self.statistic.level_up()
            self.up_block_speed()

    def up_block_speed(self):
        """Increasing blocks speed"""
        self.block_speed += 1

    def stop_block_speed(self):
        """Stopping blocks"""
        self.block_speed = 0

    @staticmethod
    def del_empty_blocks_line(blocks_line, blocks_lines):
        """Del empty blocks' line from game"""
        if len(blocks_line) == 0:
            blocks_lines.remove(blocks_line)
        return blocks_lines

    @staticmethod
    def del_block_outside_window(block, blocks_line):
        """Del block from blocks' line if it outside window"""
        if block.xcor() < -470:
            blocks_line.remove(block)
        return blocks_line
