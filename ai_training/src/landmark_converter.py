import mediapipe as mp


from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
landmarker = vision.HandLandmarker.create_from_options(options)

landmarker = vision.HandLandmarker.create_from_options(options)

# Load image
mp_image = mp.Image.create_from_file("fist.jpg")

# Detect
result = landmarker.detect(mp_image)

if result.hand_landmarks:
    landmarks = result.hand_landmarks[0] # 21 points, each with x,y,z, so there is a total of 63 points. it's a pointer

    feature_vector = []
    for lm in landmarks:
        feature_vector.extend([lm.x, lm.y, lm.z])

    print("output feature vector:")
    print(feature_vector)
else:
    print("No hand detected.")
