import pygame as pg
from UI_settings import UI_settings

class Score:
    def __init__(self):
        self.left_score = 0
        self.right_score = 0
        self.font = pg.font.Font(UI_settings.score_font)

    def add_point_left(self):
        self.left_score += 1

    def add_point_right(self):
        self.right_score += 1
        
    def reset_scores(self):
        self.left_score = 0
        self.right_score = 0

    def get_score(self):
        return (self.left_score, self.right_score)
