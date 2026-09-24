# BAVK — Technical To-Do / Development Notes

## Current baseline

The stable baseline is a working USB HID controller with:

- Raspberry Pi Pico RP2040
- CircuitPython 10.3.0
- Encoder on GP2 / GP3
- Encoder button on GP4
- WS2812B 16-LED ring on GP0
- Volume up/down HID events
- System mute HID event
- `Win + Alt + K` microphone mute action
- LED status indication
- NeoPixel dependencies stored in the repository

## Completed

### USB HID
- [x] Volume up
- [x] Volume down
- [x] System mute
- [x] Keyboard HID `Win + Alt + K`
- [x] Windows 11 verification

### Encoder
- [x] Quadrature decoding
- [x] One volume event per complete detent
- [x] Button debounce
- [x] Short-press detection
- [x] Long-press detection
- [x] 500 ms long-press threshold

### LED ring
- [x] WS2812B 16-pixel integration
- [x] White steady state
- [x] Red steady microphone-mute state
- [x] Orange breathing system-mute state
- [x] Red breathing system+microphone-mute state
- [x] Green 2-second microphone-unmute confirmation
- [x] LED priority handling
- [x] NeoPixel libraries added to repository

### Repository
- [x] Active implementation consolidated in `code.py`
- [x] Older tests moved to `Archive/`
- [x] NeoPixel dependencies stored under `lib/`
- [x] Repository synchronized with GitHub

## Known limitations

### Host-state feedback

BAVK tracks mute states locally. The LED therefore represents the state BAVK believes it has set, rather than independently reading the actual Windows audio/microphone state.

If Windows or another application changes mute state outside BAVK, the LED will not automatically follow that external change.

### Microphone mute

Short press sends `Win + Alt + K`. This is useful for applications supporting that shortcut. On a system without a supported application active, Windows may report that no supported applications are in use.

The current implementation intentionally keeps this behavior unchanged.

### Encoder/button interference

Testing showed electrical/mechanical coupling in the encoder module can affect the button signal during rotation.

Current button debounce is 20 ms.

A possible future mitigation is a short software lockout after encoder movement. This is not part of the stable baseline.

### USB maintenance mode

A boot-time maintenance mode was investigated, intended to enable the CIRCUITPY drive only when the encoder button is held during boot/reset.

The tested implementation did not behave reliably on the current third-party RP2040 board.

This remains a future investigation item. The stable `boot.py` should not be changed without a reproducible test case.

## Planned improvements

### Encoder acceleration

Proposed behavior:

- Normal rotation: 1x
- Fast rotation: 2x
- First detent after stopping: 1x
- First detent after direction change: 1x
- Direction change resets acceleration
- Proposed fast threshold: approximately 150 ms between complete detents

This is intentionally not implemented in the stable baseline.

### Host-state synchronization

Investigate whether BAVK can obtain reliable Windows audio and microphone mute state without a custom driver or background application.

Goal: make the LED represent actual host state rather than only BAVK's local state.

### Encoder/button signal isolation

Investigate:
- software lockout after encoder movement
- hardware debounce/filtering
- alternative encoder module
- grounding/wiring improvements

### USB maintenance mode

Revisit boot-time USB mass-storage control after the current hardware/software behavior is better understood.

## Design decisions

### No volume-level LED indicator

The LED ring is used for device-state feedback, not as a volume meter.

### No host application

Core BAVK functionality is intended to remain driverless and based on standard HID behavior.

### Stable baseline first

New features should be implemented incrementally and tested independently. The current `code.py` is the known-good baseline before introducing acceleration, host-state synchronization or USB maintenance-mode changes.
