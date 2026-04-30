from stable_baselines3 import PPO
from air_hockey_env import AirHockeyEnv

env = AirHockeyEnv()
obs, _ = env.reset()

model_path = "bestOneYet.zip"

try:
    model = PPO.load(model_path, env=env)
    print(f"Załadowano model: {model_path}")
except FileNotFoundError:
    print("Błąd: Nie znaleziono pliku modelu! Uruchom najpierw train.py.")
    exit()

print("Rozpoczynam grę testową...")

while True:
    action, _ = model.predict(obs, deterministic=True)

    obs, reward, terminated, truncated, info = env.step(action)

    env.render()

    if terminated or truncated:
        obs, _ = env.reset()
