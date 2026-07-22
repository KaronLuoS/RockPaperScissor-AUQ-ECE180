"""
Runs on the Uno Q via App Lab. Receives hand-landmark feature vectors
from laptop_sender.py (running on your laptop) over HTTP, classifies
the gesture with the tflite model, and pushes the result to the Web UI.

No camera, no mediapipe, no opencv needed here anymore - just numpy and
ai-edge-litert. This sidesteps the whole aarch64 mediapipe build/libGL
mess entirely.

Add the "web_ui" Brick to this app in App Lab before running.
"""

from arduino.app_utils import App
from arduino.app_bricks.web_ui import WebUI

from gesture_classifier import GestureClassifier

ui = WebUI()
classifier = GestureClassifier()

def handle_landmarks(body: dict):
    """
    Expects POST JSON body: {"features": [63 floats]}
    """
    features = body.get("features")

    label, confidence = classifier.predict(features)
    if label is None:
        return {"label": "invalid", "confidence": 0.0}

    result = {"label": label, "confidence": round(confidence, 3)}
    ui.send_message("gesture", result)
    return result
    


ui.expose_api("POST", "/landmarks", handle_landmarks)

App.run()