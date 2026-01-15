import pygame as pg

from Screen_helper import Screen_helper


class Board:
    def __init__(self):
        self.set_all()

    def set_all(self):
        self.screen = Screen_helper.get_screen()
        self.screen_size = Screen_helper.get_size()
        self.board_offset = 0.1
        self.board_size = 0.8
        self.board_pos = (self.screen_size[0] * 0.1, self.screen_size[1] * 0.1)
        self.board_size = (self.screen_size[0] * 0.8, self.screen_size[1] * 0.8)
        self.middle_line_start_pos = (
            self.board_pos[0] + self.board_size[0] / 2,
            self.board_pos[1],
        )
        self.middle_line_end_pos = (
            self.board_pos[0] + self.board_size[0] / 2,
            self.board_pos[1] + self.board_size[1],
        )
        self.left_goal_line_start_pos = (
            self.board_pos[0],
            self.board_pos[1] + self.board_size[1] * 0.4,
        )

        self.left_goal_line_end_pos = (
            self.board_pos[0],
            self.board_pos[1] + self.board_size[1] * 0.6,
        )

        self.right_goal_line_start_pos = (
            self.board_pos[0] + self.board_size[0],
            self.board_pos[1] + self.board_size[1] * 0.4,
        )

        self.right_goal_line_end_pos = (
            self.board_pos[0] + self.board_size[0],
            self.board_pos[1] + self.board_size[1] * 0.6,
        )

    def update_board_size(self):
        self.set_all()

    def draw(self):
        pg.draw.rect(self.screen, "pink", (self.board_pos, self.board_size), width=5)
        pg.draw.line(
            self.screen, "pink", self.middle_line_start_pos, self.middle_line_end_pos
        )
        pg.draw.line(
            self.screen,
            "green",
            self.left_goal_line_start_pos,
            self.left_goal_line_end_pos,
            width=6,
        )
        pg.draw.line(
            self.screen,
            "green",
            self.right_goal_line_start_pos,
            self.right_goal_line_end_pos,
            width=6,
        )

    def get_board_bounds(self):
        top_x = self.board_pos[1]
        bottom_x = self.board_pos[1] + self.board_size[1]
        left_y = self.board_pos[0]
        right_y = self.board_pos[0] + self.board_size[0]
        middle_y = self.middle_line_start_pos[0]
        return (top_x, bottom_x, left_y, right_y, middle_y)

    def get_goals_bounds(self):
        top = self.left_goal_line_start_pos[1]
        bottom = self.left_goal_line_end_pos[1]
        return (top, bottom)
