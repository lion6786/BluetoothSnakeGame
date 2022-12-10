import time
import evdev
from evdev import InputDevice


# If there are no devices available then wait until there are
def get_user_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    while len(devices) == 0:
        print("There are currently no devices available to connect to. Ensure the controller you would like to use is "
              "connected and able to be paired...")
        while len(devices) == 0:  # Check for available devices every half second
            time.sleep(.5)
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    else:
        # List out the available devices
        for device in devices:
            print(f"\nThis device is available:\n{device}")

    device_connected = False
    user_device = input(
        "\nEnter the event number of the device you would like to connect (if wanting event20, enter 20): ")
    print(f"\nYou chose event: {user_device}")

    while not device_connected:
        try:
            gamepad = InputDevice("/dev/input/event" + user_device)
            print(f"\nSuccessfully connected to {device.name}")
            device_connected = True

        except (PermissionError, FileNotFoundError):
            print("\nUnable to connect to device\n")
            user_device = input("Enter the device event of the device you would like to connect (ex: eventxx): \n")
            print(f"You chose event: {user_device}")

    return gamepad



"""user_device_path = get_user_device().path
print(user_device_path)"""
