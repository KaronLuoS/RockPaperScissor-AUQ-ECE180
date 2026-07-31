import random
import threading
import time

from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI

from gesture_classifier import GestureClassifier

ui = WebUI()
classifier = GestureClassifier()

# Bridge.call() is a single request/response channel
_bridge_lock = threading.Lock()


def bridge_call(*args, **kwargs):
    with _bridge_lock:
        return Bridge.call(*args, **kwargs)


# The button wins immediately over anything in progress. .
_session_id = 0
_session_id_lock = threading.Lock()


def new_session():
    global _session_id
    with _session_id_lock:
        _session_id += 1
        return _session_id


ANIM = {
    "title": 0, "you": 1, "win": 2, "lose": 3, "draw": 4,
    "rock": 5, "paper": 6, "scissors": 7, "hold": 8, "nohand": 9,
    "countdown": 10, "countup": 11,
    "waiting": 12, "gamestart": 13, "gameend": 14, "onemore": 15,
}
NAMES = ["rock", "paper", "scissors"]

# --- round-triggering tuning ---
CONFIDENCE_THRESHOLD = 0.50     # ignore low-confidence reads when locking in a move
STABLE_FRAMES_REQUIRED = 4      # consecutive confident, matching reads before locking in
COOLDOWN_SECONDS = 2.0          # minimum gap between rounds
BUTTON_POLL_SECONDS = 0.1       # how often to check the physical start/stop button

# --- state ---
_last_label = None
_stable_count = 0
_last_round_time = 0.0
_player_score = 0
_computer_score = 0
_game_active = True  # gated by the physical button

#check if consequtive anime (start+intro+countup/game+result) is in progress
_busy = False


# --- animation helpers ---

def play_wait(name, session=None):
    """
    Plays `name` and blocks until it finishes. If `session` is given, this
    bails out early (returning False) the moment _session_id no longer
    matches -- i.e. a newer button press has superseded whatever sequence
    this call belongs to. Returns True if the animation completed normally.
    """
    if session is not None and session != _session_id:
        return False

    bridge_call("play", ANIM[name], False)
    while bridge_call("is_playing"):
        if session is not None and session != _session_id:
            return False
        time.sleep(0.05)

    # check immediate stop for button input
    if session is not None and session != _session_id:
        return False
    return True


def play_loop_start(name):
    bridge_call("play", ANIM[name], True)


def stop_anim():
    bridge_call("stop_anim")


def judge(player, machine):
    if player == machine:
        return 2  # draw
    return 0 if (player - machine) % 3 == 1 else 1  # 0 = player wins, 1 = machine wins


# --- game logic ---

def play_round(player_label, session):
    """
    Plays one round against a locked-in player gesture: reveals the
    machine's move, judges the outcome, updates the running score, and
    plays the corresponding animations. Returns the round summary dict, or
    None if a button press interrupted the round partway through.
    """
    global _player_score, _computer_score

    stop_anim()

    player = NAMES.index(player_label)
    machine = random.randint(0, 2)
    if not play_wait(NAMES[machine], session=session):
        return None

    result = judge(player, machine)
    if result == 2:
        if not play_wait("draw", session=session):
            return None
        outcome = "draw"
    else:
        if not play_wait("you", session=session):
            return None
        if result == 0:
            if not play_wait("win", session=session):
                return None
            outcome = "win"
            _player_score += 1
        else:
            if not play_wait("lose", session=session):
                return None
            outcome = "lose"
            _computer_score += 1

    # back to idle, waiting for the next gesture -- but only if this
    # session is still current; otherwise the button already started its
    # own sequence and we shouldn't stomp on it.
    if session == _session_id:
        play_loop_start("hold")

    return {
        "player_move": player_label,
        "computer_move": NAMES[machine],
        "outcome": outcome,
        "player_score": _player_score,
        "computer_score": _computer_score,
    }


def start_round(label):
    """
    Runs a full round as one unbreakable sequence (from the HTTP intake's
    point of view): sets _busy so no other frame can be processed while it
    runs, and always clears it afterward -- even if play_round() raises --
    so a stray exception can never leave the game stuck forever.
    """
    global _busy, _last_round_time

    session = _session_id
    _busy = True
    try:
        round_result = play_round(label, session)
        if round_result is not None:
            ui.send_message("round_result", round_result)
    finally:
        _busy = False
        _last_round_time = time.time()


# --- start/stop button ---

def check_start_stop_button():
    """
    Runs in a background thread, polling the MCU for a new button press
    (button_pressed() on the sketch clears its own flag on read, so each
    physical press is only counted once). Always allowed to run regardless
    of _busy -- the button is the one thing that can interrupt anything.
    """
    global _game_active, _player_score, _computer_score, _busy

    while True:
        try:
            if bridge_call("button_pressed"):
                session = new_session()  # supersedes any sequence in flight
                stop_anim()              # belt-and-suspenders; MCU already cut it locally
                _game_active = not _game_active
                _busy = True
                try:
                    if _game_active:
                        _player_score = 0
                        _computer_score = 0
                        print("=== GAME START ===")
                        play_wait("gamestart", session=session)
                        play_wait("title", session=session)
                        play_wait("countup", session=session)
                        if session == _session_id:
                            play_loop_start("hold")
                    else:
                        print("=== GAME END ===")
                        play_wait("gameend", session=session)
                        if session == _session_id:
                            play_loop_start("waiting")
                finally:
                    _busy = False
        except Exception as exc:
            print(f"button poll error: {exc}")
        time.sleep(BUTTON_POLL_SECONDS)


# --- HTTP intake ---

def handle_landmarks(body: dict):
    """
    Expects POST JSON body: {"features": [63 floats]}
    """
    global _last_label, _stable_count, _last_round_time

    if not _game_active or _busy:
        # Game is off, or an unbreakable sequence (intro/round/outro) is
        # playing -- ignore the request entirely, don't even run the
        # classifier, so a gesture can never sneak a round in mid-sequence.
        return {"label": "idle", "confidence": 0.0}

    features = body.get("features")

    label, confidence = classifier.predict(features)
    if label is None:
        return {"label": "invalid", "confidence": 0.0}

    result = {"label": label, "confidence": round(confidence, 3)}
    ui.send_message("gesture", result)  # live per-frame feedback

    now = time.time()
    if (now - _last_round_time) < COOLDOWN_SECONDS:
        return result

    is_locked_candidate = label != "none" and confidence >= CONFIDENCE_THRESHOLD
    if is_locked_candidate and label == _last_label:
        _stable_count += 1
    else:
        _stable_count = 0
    _last_label = label

    if _stable_count >= STABLE_FRAMES_REQUIRED:
        _stable_count = 0
        start_round(label)

    return result


ui.expose_api("POST", "/landmarks", handle_landmarks)

play_loop_start("waiting")  # idle until the button starts a game
threading.Thread(target=check_start_stop_button, daemon=True).start()

App.run()
