from stable_baselines3 import PPO
from air_hockey_env import AirHockeyEnv

models_dir = "models/PPO"
log_dir = "logs"

env = AirHockeyEnv()
env.reset()

# 1. TUTAJ WPISUJESZ NUMER MODELU DO ZAŁADOWANIA
STARTING_STEP = 9710000
model_path = f"{models_dir}/{STARTING_STEP}.zip"
#model_path = f"bestOneYet.zip"

model = PPO.load(model_path, env=env, tensorboard_log=log_dir)

print(f"Wznowiono trening z pliku: {model_path}")
print("Kontynuuje naukę...")

TIMESTEPS = 10000

iters = STARTING_STEP // TIMESTEPS

while True:
    iters += 1

    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)

    current_step = TIMESTEPS * iters
    model.save(f"{models_dir}/{current_step}")
    print(f"Zapisano model: {models_dir}/{current_step}.zip")
