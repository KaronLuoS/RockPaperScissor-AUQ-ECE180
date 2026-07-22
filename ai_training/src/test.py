"""
Step 3: Try the trained classifier live on your laptop webcam,
before deploying to the Uno Q. Press 'q' to quit.
"""
 
import cv2
import joblib
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
 
MODEL_PATH = "hand_landmarker.task"
 
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
landmarker = vision.HandLandmarker.create_from_options(options)
 
clf = joblib.load("rps_classifier_rf.joblib")
le = joblib.load("label_encoder.joblib")
 
cap = cv2.VideoCapture(0)
 
while True:
    ok, frame = cap.read()
    if not ok:
        break
 
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    result = landmarker.detect(mp_image)
 
    label_text = "no hand"
    if result.hand_world_landmarks:
        hand = result.hand_world_landmarks[0]
        handedness = result.handedness[0][0].category_name
        features = []
        for lm in hand:
            x = -lm.x if handedness == "Left" else lm.x
            features.extend([x, lm.y, lm.z])
        pred = clf.predict([features])[0]
        label_text = le.inverse_transform([pred])[0]
 
        # draw landmarks (use image-space landmarks just for display)
        h, w, _ = frame.shape
        for lm in result.hand_landmarks[0]:
            cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 4, (0, 255, 0), -1)
 
    cv2.putText(frame, label_text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    cv2.imshow("RPS Classifier", frame)
 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
 
cap.release()
cv2.destroyAllWindows()