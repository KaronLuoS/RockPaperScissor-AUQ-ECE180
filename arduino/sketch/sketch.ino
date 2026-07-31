#include "Arduino_LED_Matrix.h"
#include "Arduino_RouterBridge.h"

#include "anim_title.h"
#include "anim_you.h"
#include "anim_win.h"
#include "anim_lose.h"
#include "anim_draw.h"
#include "anim_rock.h"
#include "anim_paper.h"
#include "anim_scissors.h"
#include "anim_hold.h"
#include "anim_nohand.h"
#include "anim_countdown321.h"
#include "anim_countup123.h"
#include "anim_waiting.h"
#include "anim_gamestart.h"
#include "anim_gameend.h"
#include "anim_onemore.h"

ArduinoLEDMatrix matrix;

struct Anim { const uint32_t (*f)[5]; int n; };
#define A(x) { x, (int)(sizeof(x) / sizeof(x[0])) }

Anim anims[] = {
  A(anim_title),
  A(anim_you),
  A(anim_win),
  A(anim_lose),
  A(anim_draw),
  A(anim_rock),
  A(anim_paper),
  A(anim_scissors),
  A(anim_hold),
  A(anim_nohand),
  A(anim_countdown321),
  A(anim_countup123),
  A(anim_waiting),
  A(anim_gamestart),
  A(anim_gameend),
  A(anim_onemore),
};
const int NUM_ANIMS = sizeof(anims) / sizeof(anims[0]);

int currentAnimId = -1;
int currentFrame = 0;
bool looping = false;
bool playing = false;
unsigned long frameStartMs = 0;

// --- start/stop button ---
#define BUTTON_PIN 2  // change if D2 is used elsewhere on your board

bool buttonEventPending = false;
int buttonLastState = HIGH;              // HIGH = not pressed (INPUT_PULLUP wiring)
unsigned long buttonLastChangeMs = 0;
const unsigned long BUTTON_DEBOUNCE_MS = 50;

void checkButton() {
  int reading = digitalRead(BUTTON_PIN);
  unsigned long now = millis();
  if (reading != buttonLastState && (now - buttonLastChangeMs) > BUTTON_DEBOUNCE_MS) {
    buttonLastChangeMs = now;
    buttonLastState = reading;
    if (reading == LOW) {  // pressed (active low with pull-up)
      buttonEventPending = true;
      // Cut whatever's currently displaying right now -- don't wait for
      // Python to notice the press and call stop_anim() itself. This is
      // what makes the visual cutoff feel instant regardless of how busy
      // the Linux side is.
      stop_anim();
    }
  }
}

bool button_pressed() {
  bool was_pressed = buttonEventPending;
  buttonEventPending = false;  // clear on read so each press is only counted once
  return was_pressed;
}

void drawCurrent() {
  if (currentAnimId < 0) return;
  const Anim& a = anims[currentAnimId];
  uint32_t frame[4] = {
    a.f[currentFrame][0],
    a.f[currentFrame][1],
    a.f[currentFrame][2],
    a.f[currentFrame][3]
  };
  matrix.loadFrame(frame);
}

int play(int id, bool loop_it) {
  if (id < 0 || id >= NUM_ANIMS) return -1;
  currentAnimId = id;
  currentFrame = 0;
  looping = loop_it;
  playing = true;
  frameStartMs = millis();
  drawCurrent();
  return 0;
}

bool is_playing() {
  return playing;
}

int stop_anim() {
  playing = false;
  uint32_t off[4] = {0, 0, 0, 0};
  matrix.loadFrame(off);
  return 0;
}

int read_hand() {
  static String buf = "";
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      buf.trim();
      buf.toLowerCase();
      int result = -1;
      if (buf == "rock" || buf == "r") result = 0;
      else if (buf == "paper" || buf == "p") result = 1;
      else if (buf == "scissors" || buf == "s") result = 2;
      buf = "";
      if (result >= 0) return result;
    } else {
      buf += c;
    }
  }
  return -1;
}

void setup() {
  matrix.begin();
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Bridge.begin();
  Bridge.provide("play", play);
  Bridge.provide("is_playing", is_playing);
  Bridge.provide("stop_anim", stop_anim);
  Bridge.provide("read_hand", read_hand);
  Bridge.provide("button_pressed", button_pressed);
}

void loop() {
  checkButton();  // runs every loop, independent of animation state

  if (!playing) return;
  const Anim& a = anims[currentAnimId];
  unsigned long now = millis();
  unsigned long dur = a.f[currentFrame][4];
  if (now - frameStartMs >= dur) {
    currentFrame++;
    if (currentFrame >= a.n) {
      if (looping) {
        currentFrame = 0;
      } else {
        playing = false;
        return;
      }
    }
    drawCurrent();
    frameStartMs = now;
  }
}
