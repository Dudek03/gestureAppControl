import pygame as pg


class Board:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size
        self.board_pos = (self.screen_size[0] * 0.1, self.screen_size[1] * 0.1)
        self.board_size = (self.screen_size[0] * 0.8, self.screen_size[1] * 0.8)
        self.line_start_pos = (
            self.board_pos[0] + self.board_size[0] / 2,
            self.board_pos[1],
        )
        self.line_end_pos = (
            self.board_pos[0] + self.board_size[0] / 2,
            self.board_pos[1] + self.board_size[1],
        )

    def change_board_size(self):
        self.board_pos = (self.screen_size[0] * 0.1, self.screen_size[1] * 0.1)
        self.board_size = (self.screen_size[0] * 0.8, self.screen_size[1] * 0.8)

    def draw(self):
        pg.draw.rect(self.screen, "pink", (self.board_pos, self.board_size), width=5)
        pg.draw.line(self.screen, "pink", self.line_start_pos, self.line_end_pos)

    def get_board_bounds(self):
        top_x = self.board_pos[1]
        bottom_x = self.board_pos[1] + self.board_size[1]
        left_y = self.board_pos[0]
        right_y = self.board_pos[0] + self.board_size[0]
        middle_y = self.line_start_pos[0]
        return (top_x, bottom_x, left_y, right_y, middle_y)
