import cv2
import threading
import time
import sys

try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    print("--- Success: MediaPipe loaded ---")
except Exception as e:
    print(f"--- ERROR: MediaPipe initialization failed ---")
    print(f"Details: {e}")
    sys.exit(1)

class HandTracker:
    def __init__(self, conf=0.7):
        self.mp_hands = mp_hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=conf,
            min_tracking_confidence=conf
        )
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.margin = 0.2            
        self.smoothing_factor = 0.2 

        self.hand_x = 0.5
        self.target_x = 0.5
        self.hand_y = 0.5
        self.target_y = 0.5
        
        self.is_detected = False
        self.running = True
        
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        target_fps = 60
        frame_duration = 1.0 / target_fps
        
        while self.running:
            start_time = time.time()
            
            success, frame = self.cap.read()
            if not success:
                time.sleep(0.01)
                continue
            
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0]
                node = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                
                self.target_x = node.x
                self.target_y = node.y
                self.is_detected = True
            else:
                self.is_detected = False

            self.hand_x += (self.target_x - self.hand_x) * self.smoothing_factor
            self.hand_y += (self.target_y - self.hand_y) * self.smoothing_factor
            
            elapsed = time.time() - start_time
            if elapsed < frame_duration:
                time.sleep(frame_duration - elapsed)

    def get_position(self, target_width=1280, target_height=720):
        active_range = 1.0 - (2 * self.margin)
        norm_x = (self.hand_x - self.margin) / active_range
        norm_y = (self.hand_y - self.margin) / active_range
        
        norm_x = max(0.0, min(1.0, norm_x))
        norm_y = max(0.0, min(1.0, norm_y))
        
        return (int(norm_x * target_width), int(norm_y * target_height))

    def get_hand_visible(self):
        return self.is_detected

    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        self.hands.close()
