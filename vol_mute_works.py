import time
import usb_hid

print("Waiting for USB...")
time.sleep(3)

mic_hid = usb_hid.devices[3]

print("Sending MIC MUTE")
mic_hid.send_report(bytes([0x01]))

time.sleep(2)

print("Sending MIC UNMUTE")
mic_hid.send_report(bytes([0x00]))

print("DONE")

while True:
    time.sleep(1)