import pygame as pg

from Screen_helper import Screen_helper


class Player:
    def __init__(self):
        self.screen = Screen_helper.get_screen()
        self.screen_size = Screen_helper.get_size()
        self.player_pos_curr = (800, 360)
        self.player_pos_last = (800, 360)
        self.player_vect = pg.Vector2(0, 0)
        self.player_size = min(self.screen_size[0], self.screen_size[1]) * 0.05

    def update_player_pos(self):
        self.player_pos_last = self.player_pos_curr
        self.player_pos_curr = pg.mouse.get_pos()

    def update_player_size(self):
        self.screen_size = Screen_helper.get_size()
        self.player_size = min(self.screen_size[0], self.screen_size[1]) * 0.05

    def reset(self):
        self.player_pos_curr = (800, 360)
        self.player_pos_last = (800, 360)

    def calculate_player_vector(self):
        self.player_vect = pg.math.Vector2(
            pg.math.Vector2(self.player_pos_curr)
            - pg.math.Vector2(self.player_pos_last)
        )

    def get_player_vect(self):
        return self.player_vect

    def get_player_pos(self):
        return self.player_pos_curr

    def set_player_pos(self, new_pos):
        self.player_pos_curr = new_pos

    def get_player_size(self):
        return self.player_size

    def draw(self):
        pg.draw.circle(
            self.screen, "pink", self.player_pos_curr, self.player_size, width=5
        )

    def update(self):
        self.update_player_pos()
        self.draw()
