import keyboard
import threading
import pyautogui
from configparser import ConfigParser
from config_file import config_create

# Insure config is created
config_create()

# Read the config file
config = ConfigParser()
config.read('config.ini')

cord_x = config.get('General', 'coordinates_x')
cord_y = config.get('General', 'coordinates_Y')


class ThreadThatPause(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._running_event = threading.Event()
        self.daemon = True

    # Start the entire thread, the key to the engine
    def start(self):
        super().start()
        self._running_event.set()

    # Pause the thread
    def pause(self):
        self._running_event.clear()

    # Start the thread again
    def resume(self):
        self._running_event.set()

    # Check if the thread on/off
    def running(self):
        return self._running_event.is_set()

    # If thread is off (false) then resume, if not (true) then pause
    def toggle(self):
        if self.running():
            self.pause()
        else:
            self.resume()


# Class for the loop to start
class MyLoop(ThreadThatPause):
    def run(self):
        while True:
            if self.running():
                pyautogui.click()
                pyautogui.moveTo(int(cord_x), int(cord_y))


# Create the thread but do not start it yet
loop = MyLoop()

# Use a list to store the loop_running variable
loop_running = [False]


# Avoid the loop from starting while running the script
def start_loop_with_key_event(e):
    # If the loop is not running then start()
    if not loop_running[0]:
        loop.start()
        loop_running[0] = True
    else:
        # Else then toggle since it already started
        loop.toggle()


def key_start():
    # Set up the keyboard event handler to start or toggle the loop
    keyboard.on_press_key(config.get('General', 'keybind'), start_loop_with_key_event)

    # Wait for a different key (e.g., "=") to exit the program
    keyboard.wait("=")
