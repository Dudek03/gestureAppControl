import pygame as pg

from Screen_helper import Screen_helper
from UI_settings import UI_settings


class Score:
    def __init__(self):
        self.left_score = 0
        self.right_score = 0
        self.screen_size = Screen_helper.get_size()
        self.padding_x = int(self.screen_size[0] * 0.04)
        self.padding_y = int(self.screen_size[1] * 0.03)
        base_scale = (self.screen_size[0] + self.screen_size[1]) / 2
        self.font_size = int(base_scale * 0.05)
        self.font = pg.font.SysFont('Arial', self.font_size, bold=True)
        self.screen = Screen_helper.get_screen()

    def add_point_left(self):
        self.left_score += 1

    def add_point_right(self):
        self.right_score += 1

    def reset_scores(self):
        self.left_score = 0
        self.right_score = 0

    def update_score_size(self):
        self.screen_size = Screen_helper.get_size()
        base_scale = (self.screen_size[0] + self.screen_size[1]) / 2
        
        self.font_size = int(base_scale * 0.05)
        self.font = pg.font.SysFont('Arial', self.font_size, bold=True)
        
        self.padding_x = int(self.screen_size[0] * 0.04)
        self.padding_y = int(self.screen_size[1] * 0.03)

    def show_score(self):
        score_str = f"{self.left_score}:{self.right_score}"
        text_surface = self.font.render(score_str, True, (255, 255, 255))
        
        center_x = self.screen_size[0] // 2
        top_y = self.screen_size[1] // 15
        
        text_rect = text_surface.get_rect(midtop=(self.screen_size[0] // 2, top_y))
        frame_rect = text_rect.inflate(self.padding_x, self.padding_y)
        
        pg.draw.rect(self.screen, (0, 0, 0), frame_rect, border_radius=10)
        pg.draw.rect(self.screen, (255, 255, 255), frame_rect, width=3, border_radius=10)
        self.screen.blit(text_surface, text_rect)
