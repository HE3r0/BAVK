import board
import busio
import displayio
import terminalio
import time
import rotaryio
import digitalio
import usb_hid

from i2cdisplaybus import I2CDisplayBus
from adafruit_debouncer import Debouncer
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_displayio_sh1106


keyboard = Keyboard(usb_hid.devices)

displayio.release_displays()

i2c = busio.I2C(board.GP17, board.GP16)
display_bus = I2CDisplayBus(i2c, device_address=0x3C)

display = adafruit_displayio_sh1106.SH1106(
    display_bus,
    width=132,
    height=64,
    rotation=0,
)

root = displayio.Group()
display.root_group = root

title = label.Label(
    terminalio.FONT,
    text="Macropad",
    color=0xFFFFFF,
    x=8,
    y=10
)

status = label.Label(
    terminalio.FONT,
    text="Ready",
    color=0xFFFFFF,
    x=8,
    y=28
)

root.append(title)
root.append(status)

default_status = "Ready"
status_until = 0.0

def show_temporary(message, seconds=0.6):
    global status_until
    print(message)
    status.text = message[:20]
    status_until = time.monotonic() + seconds

def make_button(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return Debouncer(io)

confirm = make_button(board.GP0)
encoder_push = make_button(board.GP3)
back = make_button(board.GP4)
key1 = make_button(board.GP5)

encoder = rotaryio.IncrementalEncoder(board.GP1, board.GP2)
last_position = encoder.position

status.text = default_status
print("System Ready")

while True:
    confirm.update()
    encoder_push.update()
    back.update()
    key1.update()

    if confirm.fell:
        show_temporary("Confirm")

    if encoder_push.fell:
        show_temporary("Encoder Push")

    if back.fell:
        show_temporary("Back")

    if key1.fell:
        show_temporary("Ctrl+Shift+Esc")
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE)

    position = encoder.position
    if position != last_position:
        if position > last_position:
            show_temporary("CW")
        else:
            show_temporary("CCW")
        last_position = position

    if status_until and time.monotonic() > status_until:
        status.text = default_status
        status_until = 0.0

    time.sleep(0.01)
