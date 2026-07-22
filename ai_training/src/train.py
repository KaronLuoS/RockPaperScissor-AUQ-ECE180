import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf

CSV_PATH = "landmarks.csv"

# Landmark indices (MediaPipe hand model)
WRIST = 0
FINGER_MCP = {"thumb": 2, "index": 5, "middle": 9, "ring": 13, "pinky": 17}
FINGER_TIP = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}
 
def landmark_xyz(row, i):
    return np.array([row[f"x{i}"], row[f"y{i}"], row[f"z{i}"]])
 
 
def curl_features(row):
    """One extension ratio per finger: tip-to-wrist distance divided by
    mcp-to-wrist distance. ~1 or lower means curled, higher means extended.
    Returns 5 features instead of 63."""
    wrist = landmark_xyz(row, WRIST)
    feats = []
    for finger in FINGER_MCP:
        mcp = landmark_xyz(row, FINGER_MCP[finger])
        tip = landmark_xyz(row, FINGER_TIP[finger])
        mcp_dist = np.linalg.norm(mcp - wrist) + 1e-6
        tip_dist = np.linalg.norm(tip - wrist)
        feats.append(tip_dist / mcp_dist)
    return feats


df = pd.read_csv(CSV_PATH)
X = df.drop(columns=["label"]).values  
y_raw = df["label"].values

le = LabelEncoder()
y = le.fit_transform(y_raw)
print("Classes:", list(le.classes_))
print("Dataset shape:", X.shape)
 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# original model
# model = tf.keras.Sequential([
#     tf.keras.layers.Input(shape=(63,)),
#     tf.keras.layers.Dense(32, activation="relu"),
#     tf.keras.layers.Dense(16, activation="relu"),
#     tf.keras.layers.Dense(len(le.classes_), activation="softmax"),
# ])

#bigger model
model = tf.keras.Sequential([
    tf.keras.layers.Input((63,)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(len(le.classes_), activation="softmax")
])

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(X_train, y_train, validation_data=(X_test, y_test),
          epochs=100, batch_size=16, verbose=2)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open("rps_classifier.tflite", "wb") as f:
    f.write(tflite_model)
print("Saved rps_classifier.tflite")