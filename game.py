import math

import pygame as pg

pg.init()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
screen_size = pg.display.get_window_size()
clock = pg.time.Clock()
running = True
dt = 0


class Player:
    def __init__(self):
        self.player_pos_curr = (0, 0)
        self.player_pos_last = (0, 0)
        self.player_vect = pg.Vector2(0, 0)
        self.player_size = min(screen_size[0], screen_size[1]) * 0.05

    def update_player_pos(self):
        self.player_pos_last = self.player_pos_curr
        self.player_pos_curr = pg.mouse.get_pos()

    def update_player_size(self):
        self.player_size = min(screen_size[0], screen_size[1]) * 0.05

    def calculate_player_vector(self):
        self.player_vect = Vector_handler.calculate_vector(
            self.player_pos_curr, self.player_pos_last
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
        pg.draw.circle(screen, "pink", self.player_pos_curr, self.player_size, width=5)

    def update(self):
        self.update_player_pos()
        self.draw()


class Vector_handler:
    @staticmethod
    def calculate_vector(pos1, pos2):
        return pg.Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])

    @staticmethod
    def normalize_vector(vector):
        return vector.normalize()

    @staticmethod
    def get_vector_length(vector):
        return vector.length()


class Puck:
    def __init__(self):
        self.puck_pos_curr = (0, 0)
        self.puck_pos_last = (0, 0)
        self.puck_vector_normalized = pg.Vector2(0.0, 0.0)
        self.puck_vector_size = 0.0
        self.puck_size = min(screen_size[0], screen_size[1]) * 0.05

    def bounce_x(self):
        self.puck_vector_normalized[0] *= -1

    def bounce_y(self):
        self.puck_vector_normalized[1] *= -1

    def get_puck_size(self):
        return self.puck_size

    def get_puck_pos(self):
        return self.puck_pos_curr

    def get_puck_vect(self):
        return (self.puck_vector_normalized, self.puck_vector_size)

    def update(self):
        self.puck_pos_last = self.puck_pos_curr
        self.puck_pos_curr = self.puck_vector_normalized * self.puck_vector_size
        self.puck_vector_size -= 0.01

    def update_puck_size(self):
        self.puck_size = min(screen_size[0], screen_size[1]) * 0.05

    def draw(self):
        pg.draw.circle(screen, "pink", self.puck_pos_curr, self.puck_size)


class Board:
    def __init__(self):
        self.board_pos = (screen_size[0] * 0.1, screen_size[1] * 0.1)
        self.board_size = (screen_size[0] * 0.8, screen_size[1] * 0.8)
        self.line_start_pos = (
            self.board_pos[0] + self.board_size[0] / 2,
            self.board_pos[1],
        )
        self.line_end_pos = (
            self.board_pos[0] + self.board_size[0] / 2,
            self.board_pos[1] + self.board_size[1],
        )

    def change_board_size(self):
        self.board_pos = (screen_size[0] * 0.1, screen_size[1] * 0.1)
        self.board_size = (screen_size[0] * 0.8, screen_size[1] * 0.8)

    def draw(self):
        pg.draw.rect(screen, "pink", (self.board_pos, self.board_size), width=5)
        pg.draw.line(screen, "pink", self.line_start_pos, self.line_end_pos)

    def get_board_bounds(self):
        top_x = self.board_pos[1]
        bottom_x = self.board_pos[1] + self.board_size[1]
        left_y = self.board_pos[0]
        right_y = self.board_pos[0] + self.board_size[0]
        middle_y = self.line_start_pos[0]
        return (top_x, bottom_x, left_y, right_y, middle_y)


class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player()
        self.puck = Puck()

    def board_validation(self, pos, size):
        board_boundaries = self.board.get_board_bounds()
        pos = list(pos)
        # left bound
        if pos[0] - size <= board_boundaries[2]:
            pos[0] = board_boundaries[2] + size
        # right bound
        elif pos[0] + size >= board_boundaries[3]:
            pos[0] = board_boundaries[3] - size
        # top bound
        if pos[1] - size <= board_boundaries[0]:
            pos[1] = board_boundaries[0] + size
        # bottom bound
        elif pos[1] + size >= board_boundaries[1]:
            pos[1] = board_boundaries[1] - size
        pos = tuple(pos)
        return pos

    def middle_line_validation(self, side, pos):
        board_boundaries = self.board.get_board_bounds()
        pos = list(pos)
        if side == "right":
            if pos[0] <= board_boundaries[4]:
                pos[0] = board_boundaries[4]
        elif side == "left":
            if pos[0] >= board_boundaries[4]:
                pos[0] = board_boundaries[4]
        pos = tuple(pos)
        return pos

    def puck_validate(self, pos, size):
        board_boundaries = self.board.get_board_bounds()
        pos = list(pos)
        # left bound
        if pos[0] - size <= board_boundaries[2]:
            self.puck.bounce_x()
        # right bound
        elif pos[0] + size >= board_boundaries[3]:
            self.puck.bounce_x()
        # top bound
        if pos[1] - size <= board_boundaries[0]:
            self.puck.bounce_y()
        # bottom bound
        elif pos[1] + size >= board_boundaries[1]:
            self.puck.bounce_y()
        pos = tuple(pos)
        # TODO
        return pos

    def puck_player_collision(self, player_pos, player_size):
        puck_pos = self.puck.get_puck_pos()
        puck_size = self.puck.get_puck_size()
        return player_size + puck_size <= math.sqrt(
            (player_pos[0] + puck_pos[0]) ** 2 + (player_pos[1] + puck_pos[1]) ** 2
        )

    def calculate_puck_vect_on_player_collide(self, player):
        puck_vect = self.puck.get_puck_vect()
        self.player.calculate_player_vector()
        player_vect = self.player.get_player_vect()
        player_vect_len = Vector_handler.get_vector_length(player_vect)
        player_vect_norm = Vector_handler.normalize_vector(player_vect)
        collide_vect = Vector_handler.calculate_vector(
            self.player.get_player_pos, self.puck.get_puck_pos
        )
        collide_vect = Vector_handler.normalize_vector(collide_vect)

    def on_display_resize(self):
        self.player.update_player_size()
        self.board.change_board_size()

    def update_player(self):
        self.player.update_player_pos()
        player_pos = self.player.get_player_pos()
        player_size = self.player.get_player_size()
        pos_in_board = self.board_validation(player_pos, player_size)
        pos_line = self.middle_line_validation("right", pos_in_board)
        self.player.set_player_pos(pos_line)

    def draw(self):
        self.player.draw()
        self.board.draw()

    def update(self):
        self.update_player()
        self.draw()


game = Game()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.VIDEORESIZE:
            game.on_display_resize()
    screen_size = pg.display.get_window_size()
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    game.update()
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pg.display.flip()

    dt = clock.tick(60) / 1000

pg.quit()
