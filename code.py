import board
import digitalio
import time
import math
import neopixel

import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


# ============================================================
# WS2812B
# ============================================================

NUM_PIXELS = 16
LED_BRIGHTNESS = 0.10

pixels = neopixel.NeoPixel(
    board.GP0,
    NUM_PIXELS,
    brightness=LED_BRIGHTNESS,
    auto_write=False,
)


# ============================================================
# COLORS
# ============================================================

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 80, 0)


def set_led(color):
    pixels.fill(color)
    pixels.show()


# ============================================================
# STATES
# ============================================================

mic_muted = False
system_muted = False

# Temporary green confirmation
green_until = 0

# LED animation update
last_led_update = 0


# ============================================================
# LED CONTROL
# ============================================================

def update_led():
    global last_led_update

    now = time.monotonic()

    # --------------------------------------------------------
    # Green confirmation has highest priority
    # --------------------------------------------------------

    if now < green_until:

        set_led(GREEN)
        return


    # --------------------------------------------------------
    # System sound MUTED
    # --------------------------------------------------------

    if system_muted:

        # Breathing animation
        if now - last_led_update >= 0.03:

            last_led_update = now

            # 1.8 second breathing cycle
            phase = (now % 1.8) / 1.8

            brightness = (
                0.20
                + 0.55 * (
                    0.5
                    + 0.5 * math.sin(
                        phase * 2 * math.pi
                    )
                )
            )

            if mic_muted:

                # --------------------------------------------
                # System MUTED + Mic MUTED
                # RED breathing
                # --------------------------------------------

                color = (
                    int(RED[0] * brightness),
                    int(RED[1] * brightness),
                    int(RED[2] * brightness),
                )

            else:

                # --------------------------------------------
                # System MUTED + Mic ON
                # ORANGE breathing
                # --------------------------------------------

                color = (
                    int(ORANGE[0] * brightness),
                    int(ORANGE[1] * brightness),
                    int(ORANGE[2] * brightness),
                )

            pixels.fill(color)
            pixels.show()

        return


    # --------------------------------------------------------
    # System sound ON
    # --------------------------------------------------------

    if mic_muted:

        # Mic MUTED
        set_led(RED)

    else:

        # Everything normal
        set_led(WHITE)


# ============================================================
# ENCODER
# ============================================================

s1 = digitalio.DigitalInOut(board.GP2)
s1.direction = digitalio.Direction.INPUT
s1.pull = digitalio.Pull.UP

s2 = digitalio.DigitalInOut(board.GP3)
s2.direction = digitalio.Direction.INPUT
s2.pull = digitalio.Pull.UP


# ============================================================
# ENCODER BUTTON
# ============================================================

key = digitalio.DigitalInOut(board.GP4)
key.direction = digitalio.Direction.INPUT
key.pull = digitalio.Pull.UP


# ============================================================
# ENCODER STATE
# ============================================================

last = (s1.value << 1) | s2.value
position = 0

transition = {
    (0, 1): -1,
    (1, 3): -1,
    (3, 2): -1,
    (2, 0): -1,

    (0, 2): 1,
    (2, 3): 1,
    (3, 1): 1,
    (1, 0): 1,
}


# ============================================================
# BUTTON DEBOUNCE
# ============================================================

key_state = key.value
key_candidate = key_state
key_candidate_time = time.monotonic()

DEBOUNCE_MS = 20
LONG_PRESS_MS = 500

press_start = 0


# ============================================================
# HID
# ============================================================

consumer_control = ConsumerControl(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # --------------------------------------------------------
    # Update LED
    # --------------------------------------------------------

    update_led()


    # --------------------------------------------------------
    # Encoder rotation
    # --------------------------------------------------------

    current = (s1.value << 1) | s2.value

    if current != last:

        movement = transition.get((last, current), 0)

        if movement:

            position += movement

            if position >= 4:

                print("VOLUME UP")

                consumer_control.send(
                    ConsumerControlCode.VOLUME_INCREMENT
                )

                position = 0

            elif position <= -4:

                print("VOLUME DOWN")

                consumer_control.send(
                    ConsumerControlCode.VOLUME_DECREMENT
                )

                position = 0

        last = current


    # --------------------------------------------------------
    # Encoder button
    # --------------------------------------------------------

    current_key = key.value

    if current_key != key_candidate:

        key_candidate = current_key
        key_candidate_time = time.monotonic()

    elif current_key != key_state:

        elapsed_ms = (
            time.monotonic() - key_candidate_time
        ) * 1000

        if elapsed_ms >= DEBOUNCE_MS:

            key_state = current_key


            # ------------------------------------------------
            # Button pressed
            # ------------------------------------------------

            if key_state is False:

                press_start = time.monotonic()

                print("KEY DOWN")


            # ------------------------------------------------
            # Button released
            # ------------------------------------------------

            else:

                duration_ms = (
                    time.monotonic() - press_start
                ) * 1000


                # ============================================
                # LONG PRESS
                # System sound mute
                # ============================================

                if duration_ms >= LONG_PRESS_MS:

                    system_muted = not system_muted

                    consumer_control.send(
                        ConsumerControlCode.MUTE
                    )

                    if system_muted:

                        print("SYSTEM MUTE")

                    else:

                        print("SYSTEM UNMUTE")


                # ============================================
                # SHORT PRESS
                # Microphone mute
                # ============================================

                else:

                    mic_muted = not mic_muted

                    keyboard.send(
                        Keycode.GUI,
                        Keycode.ALT,
                        Keycode.K
                    )

                    if mic_muted:

                        # ------------------------------------
                        # Mic MUTE
                        # ------------------------------------

                        print("MICROPHONE MUTE")

                        green_until = 0

                    else:

                        # ------------------------------------
                        # Mic UNMUTE
                        # ------------------------------------

                        print("MICROPHONE UNMUTE")

                        green_until = (
                            time.monotonic() + 2.0
                        )


                print("KEY UP")


    time.sleep(0.001)