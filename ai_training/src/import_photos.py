import os
import shutil

# Path containing all the images
train_dir = r"../karonlan-RPC-Pictures/testing"
data_dir = r"../data"

# Labels you expect
labels = ["Rock", "Paper", "Scissor","None"]

# Move each image into the correct folder
for filename in os.listdir(train_dir):
    filepath = os.path.join(train_dir, filename)

    if filename.startswith("Rock"):
        label = "Rock"
        destination = os.path.join(data_dir, "rock", filename)
    elif filename.startswith("Paper"):
        label = "Paper"
        destination = os.path.join(data_dir, "paper", filename)
    elif filename.startswith("Scissor"):
        label = "Scissor"
        destination = os.path.join(data_dir, "scissors", filename)
    else:
        label = "None"
        destination = os.path.join(data_dir, "none", filename)

    shutil.move(filepath, destination)
    print(f"Moved {filename} -> {label}")