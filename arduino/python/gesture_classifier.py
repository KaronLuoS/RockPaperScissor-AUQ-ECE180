"""
Loads the trained .tflite gesture model and runs inference on a
63-length hand-landmark feature vector (from landmark_extractor.py).
"""

import numpy as np
from pathlib import Path

try:
    import ai_edge_litert.interpreter as tflite
except ImportError:
    import tflite_runtime.interpreter as tflite
MODEL_PATH =  str(Path(__file__).resolve().parent / "rps_classifier.tflite")

CLASSES = ["none", "paper", "rock", "scissors"]


class GestureClassifier:
    def __init__(self, model_path=MODEL_PATH):
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # If the model is quantized, these will be non-(0.0, 0) and we
        # need to rescale float features into the quantized input range.
        self._in_scale, self._in_zero_point = self.input_details[0].get(
            "quantization", (0.0, 0)
        )

    def predict(self, features):
        """
        features: list/array of 63 floats (x0,y0,z0, ..., x20,y20,z20)
        Returns (label, confidence) or (None, 0.0) if input is invalid.
        """
        if features is None or len(features) != 63:
            return None, 0.0

        dtype = self.input_details[0]["dtype"]
        arr = np.array([features], dtype=np.float32)

        if self._in_scale and dtype in (np.int8, np.uint8):
            # Quantized model: rescale float features into int8/uint8 range
            arr = (arr / self._in_scale + self._in_zero_point).astype(dtype)
        else:
            arr = arr.astype(dtype)

        self.interpreter.set_tensor(self.input_details[0]["index"], arr)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]["index"])[0]

        out_scale, out_zero_point = self.output_details[0].get("quantization", (0.0, 0))
        if out_scale:
            output = (output.astype(np.float32) - out_zero_point) * out_scale

        best_idx = int(np.argmax(output))
        confidence = float(output[best_idx])
        label = CLASSES[best_idx] if best_idx < len(CLASSES) else str(best_idx)
        return label, confidence


if __name__ == "__main__":
    # Quick smoke test with a dummy all-zero feature vector
    clf = GestureClassifier()
    dummy = [0.0] * 63
    print(clf.predict(dummy))