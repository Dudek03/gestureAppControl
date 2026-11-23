# gestureAppControl — Vision-Controlled Air Hockey & Reinforcement Learning AI

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-00B140)](https://www.pygame.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-0097A7)](https://developers.google.com/mediapipe)
[![Ultralytics YOLO](https://img.shields.io/badge/Ultralytics-YOLO%20%2B%20OpenVINO-00FFFF?logo=intel&logoColor=black)](https://docs.ultralytics.com/)
[![Stable-Baselines3](https://img.shields.io/badge/RL-PPO%20%2F%20Gymnasium-FF6F00)](https://stable-baselines3.readthedocs.io/)

An interactive Air Hockey game combining **real-time webcam hand-gesture tracking** with a **Reinforcement Learning (PPO) opponent**. Play touch-free using either **Google MediaPipe Hands** or a **custom-trained YOLO detector accelerated with Intel OpenVINO**, or challenge the AI with a mouse—and train or evaluate custom PPO agents inside the included Gymnasium environment.

---

## Key Features

- **Dual Webcam Hand-Tracking Backends**:
  - **MediaPipe Hands (`gesture_controll.py`)**: Tracks the `MIDDLE_FINGER_MCP` landmark from 21 3D hand keypoints (`conf=0.7`, active margin `20%`).
  - **Custom YOLO + Intel OpenVINO Model (`gesture_controll_own_model.py`, `best_openvino_model/`)**: Runs an FP16 OpenVINO-exported Ultralytics YOLO detector (`320×320`, class `0: Hand raise`, `conf=0.25`, active margin `15%`) and tracks the bounding-box center.
  - Both trackers run asynchronously in background daemon threads with frame-buffer flushing and exponential smoothing (`smoothing_factor = 0.4`) for responsive, low-jitter mallet control.
- **Reinforcement Learning Air Hockey Environment (`air_hockey_env.py`)**:
  - Custom `gymnasium.Env` with a continuous 2D velocity action space `Box(-1, 1, shape=(2,))` and a 12-dimensional normalized state observation vector (puck, AI mallet, and opponent positions & velocities).
  - Shaped reward function incentivizing goal scoring, defensive shadowing behind the puck, high-speed goal-aligned strikes, and penalizing own-goals, idling, multi-hit spamming, and wall-hugging.
  - Pre-trained **Stable-Baselines3 PPO** checkpoints included (`bestOneYet.zip` plus progressive checkpoints from `2.78M` to `10.43M` timesteps).
- **Interactive Menu & 2D Physics Engine (`main.py`, `Game.py`)**:
  - Resizable Pygame UI (`1280×720` default, minimum `700×400`) to pick opponent (`Wyuczone AI` vs. `Skryptowany Bot`), input (`Myszka` vs. `Ręka (Kamera)`), and hand-tracking backend (`MediaPipe` vs. `Własny Model`).
  - Circle-circle elastic impulse collisions (`restitution = 1.0`) with overlap resolution, puck friction, wall bounces, center-line restrictions, and live scoreboard.

---

## Architecture & Pipeline

```mermaid
flowchart LR
    subgraph Input["Human Input Layer"]
        Cam["Webcam Feed\n(OpenCV 60 FPS)"]
        MP["MediaPipe Hands\n(MIDDLE_FINGER_MCP)"]
        YOLO["Custom YOLO Model\n(OpenVINO FP16 320x320)"]
        Smooth["Threaded Smoothing &\nMargin Remapping"]
        Mouse["Mouse Pointer\n(Fallback Input)"]
    end

    subgraph Agent["Opponent Decision Layer"]
        Obs["12-Dim Normalized\nObservation Vector"]
        PPO["PPO Policy\n(Stable-Baselines3)"]
        Bot["Scripted Bot\n(_move_player_script)"]
    end

    subgraph Core["Air Hockey Engine & UI"]
        Env["AirHockeyEnv\n(Gymnasium Wrapper)"]
        Phys["Game Physics\n(Elastic Collisions & Goals)"]
        UI["Pygame Renderer\n(60 FPS Resizable Window)"]
    end

    Cam --> MP
    Cam --> YOLO
    MP --> Smooth
    YOLO --> Smooth
    Smooth --> Env
    Mouse --> Env

    Env --> Obs
    Obs --> PPO
    PPO --> Env
    Bot --> Env

    Env --> Phys
    Phys --> UI
```

---

## Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Computer Vision** | OpenCV (`opencv-python`), MediaPipe (`0.10.11`), Ultralytics YOLO (`8.4.25`), Intel OpenVINO (`2026.0.0`) |
| **Reinforcement Learning** | Gymnasium (`1.2.3`), Stable-Baselines3 (`2.7.1`, PPO `MlpPolicy`), PyTorch (`2.10.0`), TensorBoard |
| **Game & Rendering** | Pygame (`2.6.1`), NumPy (`2.4.2`) |

---

## Project Structure

```text
gestureAppControl/
├── main.py                         # Main Pygame app with interactive menu (AI/Bot, Mouse/Hand, MediaPipe/OpenVINO)
├── gesture_controll.py             # Threaded HandTracker using MediaPipe Hands
├── gesture_controll_own_model.py   # Threaded HandTracker using custom OpenVINO YOLO model (also runnable standalone)
├── best_openvino_model/            # Exported Ultralytics YOLO OpenVINO IR model (best.xml, best.bin, metadata.yaml)
├── air_hockey_env.py               # Custom Gymnasium environment (12-dim obs, 2-dim continuous action, shaped rewards)
├── train.py                        # Train PPO agent from scratch (saves to models/PPO/ & logs/)
├── resume_train.py                 # Resume PPO training from a specified checkpoint step
├── test.py                         # Watch trained PPO model (bestOneYet.zip) play against scripted bot
├── play_vs_ai.py                   # Direct mouse-controlled Human vs. PPO AI match script
├── Game.py                         # Core game loop, scripted bots, elastic collision & goal detection
├── Board.py                        # Rink geometry, goal recesses & dashed markings
├── Player.py                       # Mallet state & movement handlers (mouse, hand tracker, AI velocity step)
├── Puck.py                         # Puck kinematics, friction & wall reflections
├── Score.py                        # Scoreboard rendering
├── Screen_helper.py                # Shared display surface & resize state manager
├── UI_settings.py                  # Colors, proportions & default window size (1280x720)
├── bestOneYet.zip                  # Pre-trained PPO agent checkpoint (plus 2.78M–10.43M milestone zips)
└── requirements.txt                # Pinned Python dependencies
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- A working **webcam** (required only for hand-gesture control mode; mouse mode works without a camera)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Dudek03/gestureAppControl.git
cd gestureAppControl

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

### 1. Launch the Full Game (Menu + Hand/Mouse Control)

```bash
python main.py
```

In the startup menu:
1. Choose **Opponent**: `Wyuczone AI` (loads `bestOneYet.zip` PPO policy) or `Skryptowany Bot`.
2. Choose **Control**: `Myszka` (Mouse) or `Ręka (Kamera)` (Webcam).
3. If using the camera, choose **Hand Detection Model**: `MediaPipe` or `Własny Model` (custom OpenVINO YOLO).
4. Click **`START MECZU`** to play. You control the **left mallet**; the AI/bot controls the **right mallet**.

### 2. Test the Custom OpenVINO Hand Tracker Standalone

Verify webcam capture and live screen-mapped coordinates in the terminal without launching the game:

```bash
python gesture_controll_own_model.py
```

### 3. Train, Resume, or Evaluate the PPO Agent

```bash
# Train a new PPO model from scratch (checkpoints every 10,000 steps to models/PPO/)
python train.py

# Monitor training curves in TensorBoard
tensorboard --logdir logs

# Resume training from a checkpoint (configure STARTING_STEP inside resume_train.py)
python resume_train.py

# Watch the pre-trained PPO model play against the scripted bot
python test.py

# Direct Mouse vs. AI match (update model_path inside play_vs_ai.py if needed)
python play_vs_ai.py
```

### Platform Notes

- **Camera backend**: `gesture_controll_own_model.py` opens the webcam with `cv2.CAP_DSHOW` (Windows DirectShow), while `gesture_controll.py` uses default `cv2.VideoCapture(0)` (macOS/Linux; switch to `CAP_DSHOW` on Windows if webcam startup is slow).
