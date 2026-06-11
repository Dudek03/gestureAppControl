import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame as pg

from Game import Game
from Screen_helper import Screen_helper
from UI_settings import UI_settings


class AirHockeyEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self):
        super(AirHockeyEnv, self).__init__()

        pg.init()
        screen_size = (800, 600)
        screen = pg.display.set_mode(screen_size, pg.RESIZABLE)
        Screen_helper.set_screen(screen)
        Screen_helper.set_screen_size(screen_size)
        self.game = Game(mode="training")

        # AI controls velocity in range <-1, 1>
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

        # Observation space: 12 normalized elements
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32
        )

        self.clock = pg.time.Clock()
        self.max_steps = 1000
        self.current_step = 0
        self.hit_cooldown = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.game.reset()
        self.current_step = 0
        self.hit_cooldown = 0

        return self._get_obs(), {}

    # def step(self, action):
    #     self.current_step += 1
    #
    #     # Run game frame
    #     if getattr(self, "human_playing", False):
    #         game_result = self.game.run_frame_play_vs_ai(action)
    #     else:
    #         game_result = self.game.run_frame_ai(action)
    #
    #     reward = 0.0
    #     terminated = False
    #     truncated = False
    #
    #     # Check for terminal states (goals)
    #     if game_result == 1:
    #         reward += 20.0
    #         terminated = True
    #     elif game_result == -1:
    #         reward -= 25.0
    #         terminated = True
    #
    #     # Get necessary positions as vectors
    #     puck_curr = pg.math.Vector2(self.game.puck.puck_pos_curr)
    #     player_pos_last = pg.math.Vector2(self.game.player.get_player_last_pos())
    #     player_pos_curr = pg.math.Vector2(self.game.player.get_player_pos())
    #
    #     w, h = Screen_helper.get_size()
    #     opponent_goal = pg.math.Vector2(0, h / 2)
    #
    #     # 1. POSITIONING & SHADOWING
    #     dir_to_puck = puck_curr - opponent_goal
    #     new_dist = 0
    #
    #     if dir_to_puck.length() > 0:
    #         # Normalize vector to avoid extreme coordinates
    #         dir_to_puck_norm = dir_to_puck.normalize()
    #         target_pos = puck_curr + dir_to_puck_norm * 35
    #
    #         old_dist = player_pos_last.distance_to(target_pos)
    #         new_dist = player_pos_curr.distance_to(target_pos)
    #
    #         # Reward moving towards the target position
    #         if new_dist < old_dist:
    #             reward += 0.25
    #         else:
    #             reward -= 0.2
    #
    #     # Penalize if AI is out of position
    #     if player_pos_curr.distance_to(opponent_goal) < puck_curr.distance_to(opponent_goal):
    #         reward -= 1
    #
    #     # 2. COLLISION & ACCURACY
    #     if self.hit_cooldown > 0:
    #         self.hit_cooldown -= 1
    #
    #     collision = self.game.puck_player_collision(
    #         self.game.player.get_player_pos(),
    #         self.game.player.get_player_size()
    #     )
    #
    #     if collision:
    #         # Prevent reward spamming on multi-collisions
    #         if self.hit_cooldown > 0:
    #             reward -= 5.0
    #         else:
    #             self.hit_cooldown = 8
    #
    #             puck_dir = pg.math.Vector2(self.game.puck.get_puck_vect()[0])
    #             puck_speed = self.game.puck.get_puck_vect()[1]
    #
    #             if puck_dir.length() > 0:
    #                 puck_vel = puck_dir.normalize() * puck_speed
    #                 to_opponent_goal = opponent_goal - puck_curr
    #                 alignment = puck_vel.normalize().dot(to_opponent_goal.normalize())
    #
    #                 # Reward well-aimed hits
    #                 if alignment > 0.7:
    #                     reward += 10.0 + (puck_speed * 0.3)
    #                 elif alignment < 0:
    #                     reward -= 8.0
    #
    #     # 3. MOVEMENT CONSTRAINTS
    #     # Penalize standing still only if far from target
    #     if new_dist > 20:
    #         move = player_pos_curr.distance_to(player_pos_last)
    #         if move < 2:
    #             reward -= 2
    #
    #     # Penalize hugging walls
    #     (top, bottom, left, right, _) = self.game.board.get_board_bounds()
    #     size = self.game.player.get_player_size()
    #
    #     if player_pos_curr.x >= right - size - 5:
    #         reward -= 0.2
    #     if player_pos_curr.y <= top + 5 or player_pos_curr.y >= bottom - 5:
    #         reward -= 0.1
    #
    #     # Check time limit
    #     if self.current_step >= self.max_steps:
    #         reward -= 8.0
    #         truncated = True
    #
    #     # Clip rewards to stabilize training
    #     reward = max(min(reward, 15), -15)
    #
    #     return self._get_obs(), reward, terminated, truncated, {}

    def step(self, action):
        self.current_step += 1

        # Run game frame
        if getattr(self, "human_playing", False):
            hand_pos = getattr(self, "current_hand_pos", None)
            game_result = self.game.run_frame_play_vs_ai(action, hand_pos=hand_pos)
        else:
            game_result = self.game.run_frame_ai(action)

        reward = 0.0
        terminated = False
        truncated = False

        # Check for terminal states (goals)
        if game_result == 1:
            reward += 40.0
            terminated = True
        elif game_result == -1:
            reward -= 60.0
            terminated = True

        # Get necessary positions as vectors
        puck_curr = pg.math.Vector2(self.game.puck.puck_pos_curr)
        player_pos_last = pg.math.Vector2(self.game.player.get_player_last_pos())
        player_pos_curr = pg.math.Vector2(self.game.player.get_player_pos())

        w, h = Screen_helper.get_size()
        opponent_goal = pg.math.Vector2(w, h / 2)
        # Założenie: gracz broni prawej strony boiska
        own_goal = pg.math.Vector2(0, h / 2)

        # 1. POSITIONING & SHADOWING
        dir_to_puck = puck_curr - opponent_goal
        new_dist = 0

        if dir_to_puck.length() > 0:
            # Normalize vector to avoid extreme coordinates
            dir_to_puck_norm = dir_to_puck.normalize()
            target_pos = puck_curr + dir_to_puck_norm * 35

            old_dist = player_pos_last.distance_to(target_pos)
            new_dist = player_pos_curr.distance_to(target_pos)

            # Reward moving towards the target position
            if new_dist < old_dist:
                reward += 0.45
            else:
                reward -= 0.6

        # Penalize if AI is out of position
        if player_pos_curr.distance_to(opponent_goal) < puck_curr.distance_to(opponent_goal):
            reward -= 2.5

        # 2. COLLISION & ACCURACY
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        collision = self.game.puck_player_collision(
            self.game.player.get_player_pos(), self.game.player.get_player_size()
        )

        if collision:
            # Prevent reward spamming on multi-collisions
            if self.hit_cooldown > 0:
                reward -= 7.0
            else:
                self.hit_cooldown = 4

                puck_dir = pg.math.Vector2(self.game.puck.get_puck_vect()[0])
                puck_speed = self.game.puck.get_puck_vect()[1]

                if puck_dir.length() > 0:
                    puck_vel = puck_dir.normalize() * puck_speed
                    to_opponent_goal = opponent_goal - puck_curr
                    alignment = puck_vel.normalize().dot(to_opponent_goal.normalize())


                    if alignment > 0.7:
                        base_hit_reward = 5.0
                        speed_bonus = puck_speed * 3
                        reward += base_hit_reward + speed_bonus

                        if puck_speed > 15.0:
                            reward += 20.0

                    elif alignment < 0:
                        reward -= 15.0 + (puck_speed * 0.2)

        # 3. MOVEMENT CONSTRAINTS
        # Penalize standing still only if far from target
        if new_dist > 20:
            move = player_pos_curr.distance_to(player_pos_last)
            if move < 2:
                reward -= 2

        # Penalize hugging walls
        (top, bottom, left, right, _) = self.game.board.get_board_bounds()
        size = self.game.player.get_player_size()

        if player_pos_curr.x >= right - size - 5:
            reward -= 1
        if player_pos_curr.y <= top + 5 or player_pos_curr.y >= bottom - 5:
            reward -= 0.5

        # Check time limit
        if self.current_step >= self.max_steps:
            reward -= 16.0
            truncated = True

        reward = max(min(reward, 130), -80)

        return self._get_obs(), reward, terminated, truncated, {}

    def render(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

        screen = Screen_helper.get_screen()
        screen.fill(UI_settings.get_screen_fill_color())
        self.game.draw()
        pg.display.flip()

        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        pg.quit()

    def _get_obs(self):
        puck = self.game.puck
        ai = self.game.player
        opp = self.game.opponent

        w, h = Screen_helper.get_size()

        p_pos = puck.get_puck_pos()
        p_norm_vec, p_speed = puck.get_puck_vect()

        ai_pos = ai.get_player_pos()
        ai_last = ai.get_player_last_pos()
        ai_vel_x = ai_pos[0] - ai_last[0]
        ai_vel_y = ai_pos[1] - ai_last[1]

        opp_pos = opp.get_player_pos()
        opp_last = opp.get_player_last_pos()
        opp_vel_x = opp_pos[0] - opp_last[0]
        opp_vel_y = opp_pos[1] - opp_last[1]

        # Normalize observations
        obs = np.array(
            [
                float(p_pos[0]) / w,
                float(p_pos[1]) / h,
                float(p_norm_vec[0] * p_speed) / 20.0,
                float(p_norm_vec[1] * p_speed) / 20.0,
                float(ai_pos[0]) / w,
                float(ai_pos[1]) / h,
                float(ai_vel_x) / 15.0,
                float(ai_vel_y) / 15.0,
                float(opp_pos[0]) / w,
                float(opp_pos[1]) / h,
                float(opp_vel_x) / 15.0,
                float(opp_vel_y) / 15.0,
            ],
            dtype=np.float32,
        )

        return obs
