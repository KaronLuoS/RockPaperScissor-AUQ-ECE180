"""
Captures webcam frames, extracts hand landmarks with MediaPipe, and sends the 63-float feature vector to
the Uno Q over HTTP

Usage:
    python laptop_sender.py --uno-q-ip 192.168.1.70
"""

import argparse
import time

import cv2
import requests
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "hand_landmarker.task"
SEND_INTERVAL_SEC = 0.15  # cap how often we hit the network


def build_landmarker():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.5,
    )
    return vision.HandLandmarker.create_from_options(options)


def extract_features_from_frame(landmarker, frame_bgr):
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    result = landmarker.detect(mp_image)

    if not result.hand_world_landmarks:
        return None

    hand = result.hand_world_landmarks[0]
    handedness = result.handedness[0][0].category_name

    features = []
    for lm in hand:
        x = -lm.x if handedness == "Left" else lm.x
        features.extend([x, lm.y, lm.z])
    return features


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--uno-q-ip", required=True, help="IP address of your Uno Q on the local network")
    parser.add_argument("--port", type=int, default=7000, help="Port the Uno Q's landmarks endpoint listens on")
    parser.add_argument("--camera-index", type=int, default=0)
    args = parser.parse_args()

    endpoint = f"http://{args.uno_q_ip}:{args.port}/landmarks"
    print(f"Sending landmarks to {endpoint}")

    landmarker = build_landmarker()
    cap = cv2.VideoCapture(args.camera_index)
    if not cap.isOpened():
        raise RuntimeError("Could not open laptop webcam")

    last_sent = 0.0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                continue

            cv2.imshow("Rock Paper Scissors - press q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            now = time.time()
            if now - last_sent < SEND_INTERVAL_SEC:
                continue
            last_sent = now

            features = extract_features_from_frame(landmarker, frame)
            if features is None:
                continue

            try:
                resp = requests.post(endpoint, json={"features": features}, timeout=1.0)
                if resp.ok:
                    print(resp.json())
            except requests.exceptions.RequestException as e:
                print(f"Failed to reach Uno Q: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
