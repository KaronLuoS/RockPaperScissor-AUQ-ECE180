#  Team 11 - Hand Gesture Recognition with Webcam and Display for Interactive Game
### ECE180 · Summer Session I 2026 · UC San Diego

 ![UCSD - Jacob School of Engineering](images/UCSDLogo_JSOE_BlueGold_Web.jpg)

# RockPaperScissor-AUQ

## Real-Time Rock Paper Scissors Gesture Recognition on Arduino UNO Q

A lightweight edge AI computer vision project that performs **real-time Rock Paper Scissors gesture recognition** directly on an **Arduino UNO Q** using a custom-trained **MediaPipe Model Maker classifier**.

The project explores embedded AI inference with Arduino Uno Q.

---

## Overview

# Project Features

## AI Gesture Recognition

- Real-time recognition of:
  - ✊ Rock
  - ✋ Paper
  - ✌️ Scissors
- Custom-trained MediaPipe Model Maker classifier
- Lightweight edge AI inference
- Camera-based hand gesture detection

## Interactive Game System

The Arduino UNO Q acts as the game host:

1. Player starts a game round
2. System performs a countdown on the LED matrix
3. Arduino randomly selects an gesture
4. The gesture is displayed on the LED matrix
5. Player responds with a hand gesture
6. Vision model recognizes player's move
7. System calculates the winner
8. Result is displayed to the player

---

## System Architecture
