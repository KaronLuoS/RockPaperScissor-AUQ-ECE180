import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf

CSV_PATH = "landmarks.csv"

# ---------------------------------------------------------------
# Load data
# ---------------------------------------------------------------
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


model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(63,)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(len(le.classes_), activation="softmax"),
])
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(X_train, y_train, validation_data=(X_test, y_test),
          epochs=70, batch_size=16, verbose=2)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open("rps_classifier.tflite", "wb") as f:
    f.write(tflite_model)
print("Saved rps_classifier.tflite")