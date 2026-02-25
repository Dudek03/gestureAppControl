import pygame as pg

from Screen_helper import Screen_helper
from UI_settings import UI_settings


class Board:
    def __init__(self):
        self.set_all()

    def set_all(self):
        self.screen = Screen_helper.get_screen()
        self.screen_size = Screen_helper.get_size()

        self.board_pos = (self.screen_size[0] * 0.1, self.screen_size[1] * 0.1)
        self.board_size = (
            self.screen_size[0] * 0.8, self.screen_size[1] * 0.8)

        self.left = self.board_pos[0]
        self.right = self.board_pos[0] + self.board_size[0]
        self.top = self.board_pos[1]
        self.bottom = self.board_pos[1] + self.board_size[1]

        self.goal_depth = self.screen_size[0] * 0.05

        self.goal_top_y = self.top + self.board_size[1] * 0.3
        self.goal_bottom_y = self.top + self.board_size[1] * 0.7

        self.middle_line_start = (self.left + self.board_size[0] / 2, self.top)
        self.middle_line_end = (
            self.left + self.board_size[0] / 2, self.bottom)

    def get_board_bounds(self):
        return (self.top, self.bottom, self.left, self.right, self.middle_line_start[0])

    def get_goal_y_range(self):
        return (self.goal_top_y, self.goal_bottom_y)

    def get_goal_depth(self):
        return self.goal_depth

    def update_board_size(self):
        self.set_all()

    def draw(self):
        color = UI_settings.get_board_line_color()
        width = 5

        pg.draw.line(
            self.screen, color, (self.left,
                                 self.top), (self.right, self.top), width
        )
        pg.draw.line(
            self.screen,
            color,
            (self.left, self.bottom),
            (self.right, self.bottom),
            width,
        )

        pg.draw.line(
            self.screen,
            color,
            (self.left, self.top),
            (self.left, self.goal_top_y),
            width,
        )
        pg.draw.line(
            self.screen,
            color,
            (self.left, self.goal_bottom_y),
            (self.left, self.bottom),
            width,
        )

        pg.draw.line(
            self.screen,
            color,
            (self.right, self.top),
            (self.right, self.goal_top_y),
            width,
        )

        pg.draw.line(
            self.screen,
            color,
            (self.right, self.goal_bottom_y),
            (self.right, self.bottom),
            width,
        )

        goal_left_x = self.left - self.goal_depth
        pg.draw.line(
            self.screen,
            color,
            (self.left, self.goal_top_y),
            (goal_left_x, self.goal_top_y),
            width,
        )
        pg.draw.line(
            self.screen,
            color,
            (self.left, self.goal_bottom_y),
            (goal_left_x, self.goal_bottom_y),
            width,
        )
        pg.draw.line(
            self.screen,
            color,
            (goal_left_x, self.goal_top_y),
            (goal_left_x, self.goal_bottom_y),
            width,
        )

        goal_right_x = self.right + self.goal_depth
        pg.draw.line(
            self.screen,
            color,
            (self.right, self.goal_top_y),
            (goal_right_x, self.goal_top_y),
            width,
        )
        pg.draw.line(
            self.screen,
            color,
            (self.right, self.goal_bottom_y),
            (goal_right_x, self.goal_bottom_y),
            width,
        )
        pg.draw.line(
            self.screen,
            color,
            (goal_right_x, self.goal_top_y),
            (goal_right_x, self.goal_bottom_y),
            width,
        )

        pg.draw.line(
            self.screen,
            UI_settings.get_middle_line_color(),
            self.middle_line_start,
            self.middle_line_end,
        )
