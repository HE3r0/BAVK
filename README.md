# BAVK — Big Ass Volume Knob

BAVK is a USB HID volume controller based on the Raspberry Pi Pico RP2040.

## Hardware

- Raspberry Pi Pico RP2040
- CircuitPython 10.3.0
- Rotary encoder
- 16-pixel WS2812B LED ring

### Pinout

| Function | Pico pin |
|---|---|
| Encoder S1 | GP2 |
| Encoder S2 | GP3 |
| Encoder KEY | GP4 |
| WS2812B DIN | GP0 |
| Encoder GND | GND |
| WS2812B GND | GND |
| WS2812B VCC | VBUS / USB 5V |
| Encoder 5V | Not connected |

## Functions

### Rotary encoder

- Clockwise: Volume Up
- Counter-clockwise: Volume Down
- One complete detent produces one HID volume event.

### Encoder button

Short press:
- Toggles the local microphone-mute state.
- Sends `Win + Alt + K`.
- Microphone unmute gives a green LED confirmation for 2 seconds.

Long press:
- 500 ms threshold.
- Toggles system audio mute.
- Sends standard HID `MUTE`.

## LED status

| System audio | Microphone | LED |
|---|---|---|
| Unmuted | Unmuted | White, steady |
| Unmuted | Muted | Red, steady |
| Muted | Unmuted | Orange, breathing |
| Muted | Muted | Red, breathing |
| Microphone unmute | — | Green for 2 seconds, then normal state |

The green confirmation has the highest display priority.

The LED state is based on BAVK's local state. It is not an independent read-back of the actual Windows host state.

Volume-level indication is intentionally not implemented.

## Software dependencies

The repository contains the NeoPixel dependencies:

```text
lib/
├── adafruit_pixelbuf.mpy
└── neopixel.mpy
```

BAVK also uses the Adafruit HID library (`adafruit_hid`).

Standard CircuitPython modules such as `board`, `digitalio`, `time` and `math` are provided by CircuitPython.

## Project structure

```text
BAVK/
├── Archive/
├── boot.py
├── code.py
├── README.md
├── TTD.md
└── lib/
    ├── adafruit_pixelbuf.mpy
    └── neopixel.mpy
```

`Archive/` contains older test/development files.

## USB identification

The current `boot.py` identifies the device as:

- Manufacturer: `MacioMan`
- Product: `BAVK`

The current normal configuration keeps the filesystem available as a `BAVK` drive for maintenance.

A dedicated boot-time maintenance mode without normal USB mass storage remains a future investigation item.

## Deployment

1. Install CircuitPython 10.3.0.
2. Copy the required HID library to `CIRCUITPY/lib/` if it is not already present.
3. Copy `boot.py` and `code.py`.
4. Copy `lib/neopixel.mpy` and `lib/adafruit_pixelbuf.mpy`.
5. Connect the encoder and LED ring according to the pinout.
6. Reset the board and verify HID and LED behavior.

See `TTD.md` for known limitations and future improvements.
