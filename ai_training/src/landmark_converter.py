import os
import csv
import cv2

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

DATASET_DIR = "../data"
MODEL_PATH = "hand_landmarker.task"
OUTPUT_CSV = "landmarks.csv"
CLASSES = ["rock", "paper", "scissors", "none"]

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1, min_hand_detection_confidence=0.5,)
landmarker = vision.HandLandmarker.create_from_options(options)

def extract_features(image_path):
    """Returns a 63-length list of floats, or None if no hand was found."""
    mp_image = mp.Image.create_from_file(image_path)
    if mp_image is None:
        return None
    
    result = landmarker.detect(mp_image)
    if not result.hand_landmarks:
        return None

    hand = result.hand_landmarks[0]
    features = []
    for lm in hand:
        features.extend([lm.x, lm.y, lm.z])
    return features


# # Load image
# mp_image = mp.Image.create_from_file("fist.jpg")

# # Detect
# result = landmarker.detect(mp_image)

# if result.hand_landmarks:
#     landmarks = result.hand_landmarks[0] # 21 points, each with x,y,z, so there is a total of 63 points. it's a pointer

#     feature_vector = []
#     for lm in landmarks:
#         feature_vector.extend([lm.x, lm.y, lm.z])

#     print("output feature vector:")
#     print(feature_vector)
# else:
#     print("No hand detected.")

def main():
    rows = []
    skipped = 0

    for label in CLASSES:
        folder = os.path.join(DATASET_DIR, label)
        if not os.path.isdir(folder):
            print(f"  (skipping missing folder: {folder})")
            continue

        image_files = [f for f in os.listdir(folder)
                        if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        print(f"{label}: {len(image_files)} images")

        for fname in image_files:
            path = os.path.join(folder, fname)
            features = extract_features(path)
            if features is None:
                skipped += 1
                continue
            rows.append(features + [label])

    header = [f"{axis}{i}" for i in range(21) for axis in ("x", "y", "z")] + ["label"]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"\nDone. Wrote {len(rows)} samples to {OUTPUT_CSV}")
    print(f"Skipped {skipped} images (no hand detected)")


if __name__ == "__main__":
    main()
