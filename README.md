#  Team 11 - Hand Gesture Recognition and Display for Interactive Game
### ECE180 · Summer Session I 2026 · UC San Diego

![UCSD Jacobs School of Engineering](image/ucsd-jacobs-logo.jpg)



 ## Table of Contents
 
1. [Team Members](#team-members)
2. [Abstract](#abstract)
3. [What We Promised](#what-we-promised)
4. [Accomplishments](#accomplishments)
5. [Video Demo & Photos](#video-demo--photos)
6. [Usage](#usage)
---
 
## Team Members
 
| Name | Major | Contacts | LinkedIn |
|---|---|---|---|
| Kailan Luo | ECE | kluo@ucsd.edu | [LinkedIn]() |
| Myles Guerrero | ECE | myguerrero@ucsd.edu | [LinkedIn](https://www.linkedin.com/in/myles-guerrero-54b0b5365) |
| Riku Nagareda | ECE | rnagareda@ucsd.edu| [LinkedIn]()
 
---


## Abstract

This project implements an AI-powered **Rock-Paper-Scissors** game using real-time hand gesture recognition. A laptop captures video from a webcam and uses **MediaPipe Hand Landmarker** to extract hand landmarks. These landmarks are transmitted to an **Arduino UNO Q**, which performs gesture classification and controls the game logic. The Arduino randomly selects its move, determines the winner, and displays animations and results on an LED matrix. The project demonstrates how embedded AI, computer vision, and microcontroller programming can be integrated into an interactive gaming system.

--


## What We Promised
 
### Must-Haves
- [x] Accurate real-time recognition of "Rock", "Paper", and "Scissors" gestures via camera
- [x] A fully playable "Rock-Paper-Scissors" game where the Arduino randomly chooses its move and displays it on the 
- [x] Achieve at least 95% of accuracy on hand gestures
### Nice-to-Haves
- [ ] A second game mode — Simon Says (a memory/gesture-repetition game).  
- [ ] Different Hand Gestures for recognition in Simon Say 
- [ ] Score Counter to keep track of wins & loses 

---

## Accomplishments

### Complete end-to-end AI gaming pipeline.

```text
Camera
    ↓
MediaPipe Hand Landmark Detection (Laptop)
    ↓
Hand Landmark Extraction
    ↓
Gesture Classification
    ↓
HTTP Communication
    ↓
Arduino UNO Q
    ↓
Game Logic
    ↓
LED Matrix Display
```

The entire system operates in real time and provides a smooth interactive gaming experience.

### Reliable Gesture Recognition

The system accurately recognizes the three required hand gestures:

* Rock
* Paper
* Scissors

Recognition is both responsive and reliable under normal operating conditions.

### Debounce & Confidence Threshold

To prevent accidental detections caused by transitional hand movements, we implemented a debounce system.

A gesture is only accepted when:

* Confidence ≥ **80%**
* Detected consistently across **4 consecutive frames**
* Cooldown period between game rounds

This significantly reduced false positives and improved gameplay.

### Laptop Vision Processor (MediaPipe Integration)

The laptop:

* Captures live webcam video
* Runs MediaPipe Hand Landmarker
* Extracts **21 hand landmarks**
* Produces **63 floating-point values** (x, y, z for each landmark)
* Streams landmark data to the Arduino approximately every **150 ms** via HTTP

### Arduino Game Logic

The Arduino UNO Q:

* Receives the classified gesture
* Runs the Rock-Paper-Scissors game logic
* Randomly selects its own move
* Determines the winner
* Displays animations and results on the LED matrix

### On/Off Button

A physical button was implemented to:

* Enable or disable gesture recognition
* Place the Arduino into a waiting state
* Prevent accidental game inputs when not playing


--


### What Did Not Work

**Back-of-Hand Recognition**

Gesture recognition accuracy decreases when the player presents the back of their hand instead of the palm. MediaPipe landmarks become less reliable, resulting in lower classification confidence or incorrect predictions.

**Fully Embedded AI**

Our original goal was to execute the complete AI pipeline directly on the Arduino UNO Q.

Due to hardware and software limitations, we instead split the pipeline:

* MediaPipe Hand Landmarker runs on the laptop
* Gesture classifier and game logic run on the Arduino

Although this differs from our original plan, it allowed us to achieve reliable real-time performance.
---

### If We Had Another Week
We would extend the project by adding:

* A complete Simon Says game mode
* Support for additional gestures such as:

  * Thumbs Up
  * Spider-Man
  * Peace
  * Number gestures
* A web-based user interface displaying:

  * Current game state
  * Player score
  * Match history
* Persistent score tracking across multiple rounds

---


## Video Demo
https://www.youtubeeducation.com/watch?v=s4KVJxp8604
---

## Usage
1. copy files in `/arduino` into Arduino App Lab, add WebUI brick, and run Arduino app.
3. pip install mediapipe, cv2 and argparse in pip env and run `/ai-training/laptop_sender.py` with the flag of the Arduino IP.
5. press start button and play.







