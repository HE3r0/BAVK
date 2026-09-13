from machine import Pin
import time

s1 = Pin(2, Pin.IN, Pin.PULL_UP)
s2 = Pin(3, Pin.IN, Pin.PULL_UP)
key = Pin(4, Pin.IN, Pin.PULL_UP)

last = (s1.value() << 1) | s2.value()
position = 0

transition = {
    (0, 1): 1,
    (1, 3): 1,
    (3, 2): 1,
    (2, 0): 1,

    (0, 2): -1,
    (2, 3): -1,
    (3, 1): -1,
    (1, 0): -1,
}

key_state = key.value()
key_candidate = key_state
key_candidate_time = time.ticks_ms()

DEBOUNCE_MS = 20
LONG_PRESS_MS = 500

press_start = 0

while True:

    # Encoder
    current = (s1.value() << 1) | s2.value()

    if current != last:
        movement = transition.get((last, current), 0)

        if movement:
            position += movement

            if position >= 4:
                print("CW")
                position = 0

            elif position <= -4:
                print("CCW")
                position = 0

        last = current

    # KEY
    current_key = key.value()

    if current_key != key_candidate:
        key_candidate = current_key
        key_candidate_time = time.ticks_ms()

    elif current_key != key_state:

        if time.ticks_diff(
            time.ticks_ms(),
            key_candidate_time
        ) >= DEBOUNCE_MS:

            key_state = current_key

            if key_state == 0:
                press_start = time.ticks_ms()
                print("KEY DOWN")

            else:
                duration = time.ticks_diff(
                    time.ticks_ms(),
                    press_start
                )

                if duration >= LONG_PRESS_MS:
                    print("LONG PRESS")
                else:
                    print("SHORT PRESS")

                print("KEY UP")

    time.sleep_ms(1)