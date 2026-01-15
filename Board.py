import pygame as pg

from Screen_helper import Screen_helper
from UI_settings import UI_settings


class Board:
    def __init__(self):
        self.set_all()

    def set_all(self):
        self.screen = Screen_helper.get_screen()
        self.screen_size = Screen_helper.get_size()
        self.board_pos = (self.screen_size[0] * UI_settings.get_board_pos_mul(), self.screen_size[1] * UI_settings.get_board_pos_mul())
        self.board_size = (self.screen_size[0] * UI_settings.get_board_size_mul(), self.screen_size[1] * UI_settings.get_board_size_mul())
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

    def update_board_size(self):
        self.set_all()

    def draw(self):
        pg.draw.rect(self.screen, UI_settings.get_board_line_color(), (self.board_pos, self.board_size), width=5)
        pg.draw.line(
            self.screen, UI_settings.get_middle_line_color(), self.middle_line_start_pos, self.middle_line_end_pos
        )

    def get_board_bounds(self):
        top_x = self.board_pos[1]
        bottom_x = self.board_pos[1] + self.board_size[1]
        left_y = self.board_pos[0]
        right_y = self.board_pos[0] + self.board_size[0]
        middle_y = self.middle_line_start_pos[0]
        return (top_x, bottom_x, left_y, right_y, middle_y)
