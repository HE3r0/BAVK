# BAVK - Things To Do

This file contains ideas and planned improvements for BAVK that are intentionally not part of the current known-good baseline.

## 1. Dynamic volume acceleration

### Goal

Make volume control more responsive when the encoder is turned quickly, while keeping precise control when it is turned slowly.

The current encoder logic treats one physical detent as one volume step:

- 1 detent = 4 valid S1/S2 transitions
- slow rotation -> 1 detent = Volume +/- 1

Planned behaviour:

- slow rotation -> 1 detent = +/-1 volume step
- normal rotation -> 1 detent = +/-2 volume steps
- fast rotation -> 1 detent = +/-4 volume steps

The speed should be determined from the time between consecutive detents. This should be implemented as an acceleration layer on top of the existing, working quadrature decoder rather than changing the basic encoder state machine.

Potential future refinement:

- use more gradual acceleration instead of fixed speed bands
- potentially increase the multiplier further for very fast rotation
- define sensible maximum acceleration to avoid excessive volume jumps

The current working baseline must remain unchanged until the new behaviour is implemented and tested separately.

## 2. Addressable LED ring

Add an addressable LED ring around the encoder as a visual status indicator.

### Planned basic states

Normal operation:

- LED ring -> white
- steady light

Microphone muted:

- LED ring -> red
- steady light

System audio muted:

- LED ring -> dedicated mute indication
- possible idea: a pulsing colour/effect rather than a steady colour

The exact colour and pulse pattern for system mute are still to be decided.

### Important design decision

Do NOT initially use the LED ring as a volume-level indicator.

A volume-level indicator would require BAVK to know the actual current system volume on the computer. The current design uses standard USB HID consumer-control commands to send Volume Up/Down and does not receive the computer's volume level.

The feasibility of receiving system volume state without custom drivers, background software, or another computer-side component is not yet established. Therefore the first LED implementation should focus on local BAVK states that the device already knows itself:

- normal
- microphone muted
- system audio muted

### Future investigation

If desired, investigate whether standard USB HID provides a practical, driverless way for BAVK to receive the host's current audio volume/mute state. Do not make this a dependency for the first LED-ring implementation.