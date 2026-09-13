# BAVK - Big Ass Volume Knob

Current baseline: CircuitPython 10.3.0 on Raspberry Pi Pico RP2040.

## Hardware baseline

- S1 -> GP2
- S2 -> GP3
- KEY -> GP4
- GND -> GND
- 5V -> disconnected

## Current functionality

- Encoder CW -> Volume Up
- Encoder CCW -> Volume Down
- Short press -> Microphone mute/unmute via `Win+Alt+K`
- Long press -> System audio mute/unmute
- Long press threshold: 500 ms
- KEY debounce: 20 ms
- USB HID implemented using standard CircuitPython HID
- USB identification: `MacioMan / BAVK`
- CIRCUITPY filesystem label: `BAVK`
- LED ring is not implemented yet

## Files

- `boot.py` - USB identification and `BAVK` filesystem label
- `code.py` - working BAVK controller baseline
- `sync.bat` - add, commit and push changes to `origin/main`

## USB / boot configuration

The current `boot.py` intentionally keeps the USB configuration simple. It sets the USB manufacturer/product identification and the filesystem label to `BAVK`.

The working `code.py` baseline should not be changed together with `boot.py` without testing. Earlier storage/USB remount handling caused an `USB busy` error with HID, so the current configuration is kept as the known-good baseline.