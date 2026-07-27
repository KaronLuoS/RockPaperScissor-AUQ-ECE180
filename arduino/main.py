import random
import time

from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI

from gesture_classifier import GestureClassifier

ui = WebUI()
classifier = GestureClassifier()

ANIM = {
    "title": 0, "you": 1, "win": 2, "lose": 3, "draw": 4,
    "rock": 5, "paper": 6, "scissors": 7, "hold": 8, "nohand": 9,
    "countdown": 10, "countup": 11,
    "waiting": 12, "gamestart": 13, "gameend": 14, "onemore": 15,
}
NAMES = ["rock", "paper", "scissors"]

# --- round-triggering tuning ---
CONFIDENCE_THRESHOLD = 0.80     # ignore low-confidence reads when locking in a move
STABLE_FRAMES_REQUIRED = 4      # consecutive confident, matching reads before locking in
COOLDOWN_SECONDS = 2.0          # minimum gap between rounds

# --- state ---
_last_label = None
_stable_count = 0
_round_in_progress = False
_last_round_time = 0.0
_player_score = 0
_computer_score = 0


# --- animation helpers (from the old main.py) ---

def play_wait(name):
    Bridge.call("play", ANIM[name], False)
    while Bridge.call("is_playing"):
        time.sleep(0.05)


def play_loop_start(name):
    Bridge.call("play", ANIM[name], True)


def stop_anim():
    Bridge.call("stop_anim")


def judge(player, machine):
    if player == machine:
        return 2  # draw
    return 0 if (player - machine) % 3 == 1 else 1  # 0 = player wins, 1 = machine wins


# --- game logic ---

def play_round(player_label):
    """
    Plays one round against a locked-in player gesture: stops the
    "hold" idle loop, reveals the machine's move, judges the outcome,
    updates the running score, and plays the corresponding animations.
    Returns the round summary dict.
    """
    global _player_score, _computer_score,  _last_label

    stop_anim()

    player = NAMES.index(player_label)
    machine = random.randint(0, 2)
    play_wait(NAMES[machine])

    result = judge(player, machine)
    if result == 2:
        play_wait("draw")
        outcome = "draw"
    else:
        play_wait("you")
        if result == 0:
            play_wait("win")
            outcome = "win"
            _player_score += 1
        else:
            play_wait("lose")
            outcome = "lose"
            _computer_score += 1

    # back to idle, waiting for the next gesture
    play_loop_start("hold")

    return {
        "player_move": player_label,
        "computer_move": NAMES[machine],
        "outcome": outcome,
        "player_score": _player_score,
        "computer_score": _computer_score,
    }


# --- HTTP intake (from play_round_bridge.py) ---

def handle_landmarks(body: dict):
    """
    Expects POST JSON body: {"features": [63 floats]}
    """
    global _last_label, _stable_count, _round_in_progress, _last_round_time

    features = body.get("features")

    label, confidence = classifier.predict(features)
    if label is None:
        return {"label": "invalid", "confidence": 0.0}

    result = {"label": label, "confidence": round(confidence, 3)}
    ui.send_message("gesture", result)  # live per-frame feedback


    now = time.time()
    if _round_in_progress or (now - _last_round_time) < COOLDOWN_SECONDS:
        return result

    is_locked_candidate = label != "none" and confidence >= CONFIDENCE_THRESHOLD
    if is_locked_candidate and label == _last_label:
        _stable_count += 1
    else:
        _stable_count = 0
    _last_label = label

    if _stable_count >= STABLE_FRAMES_REQUIRED:
        _round_in_progress = True
        _stable_count = 0

        round_result = play_round(label)
        ui.send_message("round_result", round_result)

        _last_round_time = time.time()
        _round_in_progress = False

    return result


ui.expose_api("POST", "/landmarks", handle_landmarks)

print("=== GAME START ===")
play_wait("gamestart")
play_wait("title")
play_wait("countup")
play_loop_start("hold")  # idle, waiting for the first gesture

App.run()