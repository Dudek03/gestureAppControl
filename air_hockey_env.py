import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame as pg

from game import Game
from Screen_helper import Screen_helper


class AirHockeyEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self):
        super(AirHockeyEnv, self).__init__()

        self.game = Game(mode="training")

        # AI continously controls speed < -1 ; 1 >
        # [vel_x, vel_y]
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

        #  [puck_x, puck_y, puck_vx, puck_vy, ai_x, ai_y]
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32
        )

        self.clock = pg.time.Clock()
        self.max_steps = 3000
        self.current_step = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.game.reset()
        self.current_step = 0

        return self._get_obs(), {}

    def step(self, action):
        self.current_step += 1

        # 1. ai step
        # return 1 (ai win), -1 (ai lose), 0 (game continous)
        game_result = self.game.run_frame_ai(action)

        # 2. (Reward Shaping)
        reward = 0
        terminated = False
        truncated = False

        if game_result == 1:
            reward = 10.0
            terminated = True
        elif game_result == -1:
            reward = -10.0
            terminated = True
        else:
            reward = -0.001

            # maybe add TODO
            # if self.game.puck_player_collision(...): reward += 0.1

        # 3. stuck safety (Truncation)
        if self.current_step >= self.max_steps:
            truncated = True
            # punish for not doing anything
            reward -= 1.0

        # 4. observation after move
        observation = self._get_obs()

        return observation, reward, terminated, truncated, {}

    def render(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

        self.game.screen.fill(self._get_bg_color())
        self.game.draw()
        pg.display.flip()

        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        pg.quit()

    def _get_obs(self):
        """Pobiera i normalizuje dane dla AI."""
        puck = self.game.puck
        ai = self.game.player

        w, h = Screen_helper.get_size()

        p_pos = puck.get_puck_pos()
        p_vel = puck.get_puck_vect()
        ai_pos = ai.get_player_pos()

        obs = np.array(
            [
                p_pos[0] / w,  # Puck X (0-1)
                p_pos[1] / h,  # Puck Y (0-1)
                p_vel[0] / 20.0,  # Puck Vx (-1 do 1)
                p_vel[1] / 20.0,  # Puck Vy (-1 do 1)
                ai_pos[0] / w,  # AI X (0-1)
                ai_pos[1] / h,  # AI Y (0-1)
            ],
            dtype=np.float32,
        )

        return obs

    def _get_bg_color(self):
        """Pomocnicza metoda do koloru tła (możesz wziąć z UI_settings)"""
        try:
            from game_engine import UI_settings

            return UI_settings.get_screen_fill_color()
        except:
            return (0, 0, 0)
