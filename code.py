import board
import digitalio
import time

s1 = digitalio.DigitalInOut(board.GP2)
s1.direction = digitalio.Direction.INPUT
s1.pull = digitalio.Pull.UP

s2 = digitalio.DigitalInOut(board.GP3)
s2.direction = digitalio.Direction.INPUT
s2.pull = digitalio.Pull.UP

key = digitalio.DigitalInOut(board.GP4)
key.direction = digitalio.Direction.INPUT
key.pull = digitalio.Pull.UP

last = (s1.value << 1) | s2.value
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

key_state = key.value
key_candidate = key_state
key_candidate_time = time.monotonic()

DEBOUNCE_MS = 20
LONG_PRESS_MS = 500

press_start = 0

while True:

    # Encoder
    current = (s1.value << 1) | s2.value

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
    current_key = key.value

    if current_key != key_candidate:
        key_candidate = current_key
        key_candidate_time = time.monotonic()

    elif current_key != key_state:

        elapsed_ms = (time.monotonic() - key_candidate_time) * 1000

        if elapsed_ms >= DEBOUNCE_MS:

            key_state = current_key

            if key_state is False:
                press_start = time.monotonic()
                print("KEY DOWN")

            else:
                duration_ms = (time.monotonic() - press_start) * 1000

                if duration_ms >= LONG_PRESS_MS:
                    print("LONG PRESS")
                else:
                    print("SHORT PRESS")

                print("KEY UP")

    time.sleep(0.001)
