import pygame as pg

from Board import Board
from Player import Player
from Puck import Puck
from Score import Score


class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player()
        self.puck = Puck()
        self.score = Score()

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

    def goal_check_y(self):
        goals_bounds = self.board.get_goals_bounds()
        puck_pos = self.puck.get_puck_pos()
        return puck_pos[1] >= goals_bounds[0] and puck_pos[1] <= goals_bounds[1]

    def check_goal_left(self):
        puck_pos = self.puck.get_puck_pos()
        puck_size = self.puck.get_puck_size()
        board_boundaries = self.board.get_board_bounds()
        return puck_pos[0] - puck_size <= board_boundaries[2] and self.goal_check_y()

    def check_goal_right(self):
        puck_pos = self.puck.get_puck_pos()
        puck_size = self.puck.get_puck_size()
        board_boundaries = self.board.get_board_bounds()
        return puck_pos[0] + puck_size >= board_boundaries[3] and self.goal_check_y()

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

    def puck_validation(self):
        pos = self.puck.get_puck_pos()
        size = self.puck.get_puck_size()
        board_boundaries = self.board.get_board_bounds()
        is_updated = False
        pos = list(pos)
        # left bound
        if pos[0] - size <= board_boundaries[2]:
            self.puck.bounce_x()
            pos[0] = board_boundaries[2] + size + 1
            is_updated = True
        # right bound
        elif pos[0] + size >= board_boundaries[3]:
            self.puck.bounce_x()
            pos[0] = board_boundaries[3] - size - 1
            is_updated = True
        # top bound
        if pos[1] - size <= board_boundaries[0]:
            self.puck.bounce_y()
            pos[1] = board_boundaries[0] + size + 1
            is_updated = True
        # bottom bound
        elif pos[1] + size >= board_boundaries[1]:
            self.puck.bounce_y()
            pos[1] = board_boundaries[1] - size - 1
            is_updated = True
        pos = tuple(pos)
        if is_updated:
            self.puck.set_puck_pos(pos)
        # TODO

    def puck_player_collision(self, player_pos, player_size):
        puck_pos = self.puck.get_puck_pos()
        puck_size = self.puck.get_puck_size()
        radius_sum = player_size + puck_size
        collision_vect = pg.math.Vector2(puck_pos) - pg.math.Vector2(player_pos)
        dist = collision_vect.length()
        return dist < radius_sum

    def calculate_puck_vect_on_player_collide(self, player):
        puck_pos = self.puck.get_puck_pos()
        puck_vect = self.puck.get_puck_vect()
        curr_puck_vect = puck_vect[0] * puck_vect[1]
        collision_vect = pg.math.Vector2(puck_pos) - pg.math.Vector2(
            player.get_player_pos()
        )
        radius_sum = self.puck.get_puck_size() + player.get_player_size()
        dist = collision_vect.length()
        if dist <= 0:
            collision_norm = pg.math.Vector2(1, 0)
        else:
            collision_norm = collision_vect.normalize()

        penetration_depth = radius_sum - dist
        puck_pos += collision_norm * penetration_depth
        self.puck.set_puck_pos(puck_pos)
        self.player.calculate_player_vector()
        relative_vel = curr_puck_vect - player.get_player_vect()
        vel_along_norm = relative_vel.dot(collision_norm)
        if vel_along_norm < 0:
            restitution = 1.0
            j = -(1 + restitution) * vel_along_norm
            curr_puck_vect += j * collision_norm
        puck_speed = curr_puck_vect.length()
        if puck_speed > 0:
            puck_vect_norm = curr_puck_vect.normalize()
        else:
            puck_vect_norm = pg.math.Vector2(0, 0)
        self.puck.set_puck_vect_len(puck_speed)
        self.puck.set_puck_vect_norm(puck_vect_norm)

    def on_display_resize(self):
        self.player.update_player_size()
        self.board.update_board_size()
        self.puck.update_puck_size()

    def update_player(self):
        self.player.update_player_pos()
        player_pos = self.player.get_player_pos()
        player_size = self.player.get_player_size()
        pos_in_board = self.board_validation(player_pos, player_size)
        pos_line = self.middle_line_validation("right", pos_in_board)
        self.player.set_player_pos(pos_line)

    def update_puck(self):
        self.puck.update()
        if self.check_goal_left():
            self.score.add_point_right()
            self.reset()
        elif self.check_goal_right():
            self.score.add_point_left()
            self.reset()

        self.puck_validation()

    def draw(self):
        self.board.draw()
        self.player.draw()
        self.puck.draw()

    def reset(self):
        self.puck.reset()
        self.player.reset()
        self.draw()
        print(self.score.get_score())

    def update(self):
        self.update_player()
        # self.update_puck()

        self.puck.update()
        if self.check_goal_left():
            self.score.add_point_right()
            self.reset()
            return
        elif self.check_goal_right():
            self.score.add_point_left()
            self.reset()
            return

        self.puck_validation()

        if self.puck_player_collision(
            self.player.get_player_pos(), self.player.get_player_size()
        ):
            self.calculate_puck_vect_on_player_collide(self.player)
        self.draw()
