import supervisor
import storage

supervisor.set_usb_identification(
    manufacturer="MacioMan",
    product="BAVK",
)

storage.remount("/", readonly=False)

mount = storage.getmount("/")
mount.label = "BAVK"

storage.remount("/", readonly=True)