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
        screen = pg.display.set_mode(screen_size)
        Screen_helper.set_screen(screen)
        Screen_helper.set_screen_size(screen_size)
        self.game = Game(mode="training")

        # AI continously controls speed < -1 ; 1 >
        # [vel_x, vel_y]
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

        #  [puck_x, puck_y, puck_vx, puck_vy, ai_x, ai_y, ai_vx, ai_vy, opp_x, opp_y, opp_vx, opp_vy]
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32
        )

        self.clock = pg.time.Clock()
        self.max_steps = 1000
        self.current_step = 0
        self.hit_cooldown = 0  # Zainicjowany cooldown

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.game.reset()
        self.current_step = 0
        self.hit_cooldown = 0  # Wyzerowany cooldown przy restarcie środowiska

        return self._get_obs(), {}

    def step(self, action):
        self.current_step += 1

        # Execute game logic for one frame based on AI action
        if getattr(self, "human_playing", False):
            game_result = self.game.run_frame_play_vs_ai(action)
        else:
            game_result = self.game.run_frame_ai(action)

        reward = 0.0
        terminated = False
        truncated = False

        # --- TERMINAL STATES ---
        # Large rewards/penalties for scoring or conceding a goal
        if game_result == 1:
            reward += 20.0
            terminated = True
        elif game_result == -1:
            reward -= 25.0
            terminated = True

        # Helper variables for positions and goal targets
        puck_curr = pg.math.Vector2(self.game.puck.puck_pos_curr)
        puck_last = pg.math.Vector2(self.game.puck.puck_pos_last)
        player_pos_last = pg.math.Vector2(self.game.player.get_player_last_pos())
        player_pos_curr = pg.math.Vector2(self.game.player.get_player_pos())

        w, h = Screen_helper.get_size()
        opponent_goal = pg.math.Vector2(0, h / 2)
        own_goal = pg.math.Vector2(w, h / 2)

        # =========================================================
        # --- 1. POSITIONING & SHADOWING
        # Encourages the AI to stay between the puck and its own goal
        # =========================================================
        dir_to_puck = puck_curr - opponent_goal

        if dir_to_puck.length() > 0:
            # Target a spot slightly behind the puck to prepare for a hit
            target_pos = puck_curr + dir_to_puck * 35

            old_dist = player_pos_last.distance_to(target_pos)
            new_dist = player_pos_curr.distance_to(target_pos)

            # Reward moving toward the optimal hitting position
            if new_dist < old_dist:
                reward += 0.25
            else:
                reward -= 0.2

        # Penalize if the AI is further from its goal than the puck (being out of position)
        if player_pos_curr.distance_to(opponent_goal) < puck_curr.distance_to(opponent_goal):
            reward -= 1

        # =========================================================
        # --- 2. COLLISION & ACCURACY
        # Handles the actual hit logic and rewards "aiming"
        # =========================================================
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        collision = self.game.puck_player_collision(
            self.game.player.get_player_pos(),
            self.game.player.get_player_size()
        )

        if collision:
            # Penalize rapid multi-collisions (flickering/glitching)
            if self.hit_cooldown > 0:
                reward -= 5.0
            else:
                self.hit_cooldown = 8  # Prevent reward spamming

                puck_dir = pg.math.Vector2(self.game.puck.get_puck_vect()[0])
                puck_speed = self.game.puck.get_puck_vect()[1]

                if puck_dir.length() > 0:
                    puck_vel = puck_dir.normalize() * puck_speed
                    to_opponent_goal = opponent_goal - puck_curr

                    # Calculate dot product to see if the hit is aimed at the goal
                    alignment = puck_vel.normalize().dot(to_opponent_goal.normalize())

                    if alignment > 0.7:  # Hit is well-aimed towards the opponent's goal
                        reward += 10.0
                        reward += puck_speed * 0.3  # Bonus for powerful shots
                    elif alignment < 0:  # Hit sent the puck backwards
                        reward -= 8.0

        # =========================================================
        # --- 3. MOVEMENT CONSTRAINTS
        # Prevents "lazy" behavior and boundary hugging
        # =========================================================

        # Penalize standing still
        move = player_pos_curr.distance_to(player_pos_last)
        if move < 2:
            reward -= 2

        # Penalty for hugging walls or staying in corners
        (top, bottom, left, right, _) = self.game.board.get_board_bounds()
        size = self.game.player.get_player_size()

        if player_pos_curr.x >= right - size - 5:
            reward -= 0.2
        if player_pos_curr.y <= top + 5 or player_pos_curr.y >= bottom - 5:
            reward -= 0.1

        # --- TIME LIMIT ---
        if self.current_step >= self.max_steps:
            reward -= 8.0
            truncated = True

        # Clip rewards to stabilize training
        reward = max(min(reward, 15), -15)

        observation = self._get_obs()
        return observation, reward, terminated, truncated, {}

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