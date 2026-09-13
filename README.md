# BAVK - Big Ass Volume Knob

Current baseline: CircuitPython 10.3.0 on Raspberry Pi Pico RP2040.

## Hardware baseline

- S1 -> GP2
- S2 -> GP3
- KEY -> GP4
- GND -> GND
- 5V -> disconnected

## Current functionality

- Encoder CW/CCW detection
- Short press detection
- Long press detection: 500 ms
- KEY debounce: 20 ms
- USB HID and LED ring are not implemented yet

## Files

- `code.py` - working CircuitPython encoder baseline
- `syc.bat` - add, commit and push changes to `origin/main`
