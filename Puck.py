import pygame as pg

from Screen_helper import Screen_helper


class Puck:
    def __init__(self):
        self.screen = Screen_helper.get_screen()
        self.screen_size = Screen_helper.get_size()
        self.puck_pos_curr = (640, 500)
        self.puck_pos_last = (640, 500)
        self.puck_vector_normalized = pg.Vector2(0.0, 0.0)
        self.puck_vector_len = 0.0
        self.puck_size = min(self.screen_size[0], self.screen_size[1]) * 0.05

    def bounce_x(self):
        self.puck_vector_normalized[0] *= -1

    def bounce_y(self):
        self.puck_vector_normalized[1] *= -1

    def set_puck_vect_norm(self, new_vect):
        self.puck_vector_normalized = new_vect

    def set_puck_vect_len(self, new_vect_len):
        self.puck_vector_len = new_vect_len

    def set_puck_pos(self, new_pos):
        self.puck_pos_last = self.puck_pos_curr
        self.puck_pos_curr = new_pos

    def get_puck_size(self):
        return self.puck_size

    def get_puck_pos(self):
        return self.puck_pos_curr

    def get_puck_vect(self):
        return (self.puck_vector_normalized, self.puck_vector_len)

    def update(self):
        self.puck_pos_last = self.puck_pos_curr
        self.puck_pos_curr += self.puck_vector_normalized * self.puck_vector_len
        if self.puck_vector_len <= 0.0:
            self.puck_vector_len = 0.0
        else:
            self.puck_vector_len -= 0.5

    def update_puck_size(self):
        self.screen_size = Screen_helper.get_size()
        self.puck_size = min(self.screen_size[0], self.screen_size[1]) * 0.05

    def draw(self):
        pg.draw.circle(self.screen, "pink", self.puck_pos_curr, self.puck_size)
