import pygame as pg
from stable_baselines3 import PPO
from air_hockey_env import AirHockeyEnv


def main():
    env = AirHockeyEnv()
    obs, _ = env.reset()

    env.human_playing = True

    env.game.opponent.is_ai = False

    models_dir = "models/PPO"
    model_path = f"{models_dir}/14000000.zip"

    print(f"Ładowanie modelu: {model_path}...")
    model = PPO.load(model_path, env=env)

    print("=======================================")
    print("MECZ ROZPOCZĘTY: CZŁOWIEK vs AI")
    print("Użyj myszki, aby sterować lewą paletką.")
    print("=======================================")

    pg.mouse.set_visible(False)

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        env.render()

        if terminated or truncated:
            obs, _ = env.reset()

    pg.mouse.set_visible(True)
    env.close()


if __name__ == "__main__":
    main()
