import threading
import tkinter as tk
import keyboard
from configparser import ConfigParser
from listener import key_start
from get_coordinates import coordinate_get


class CustomKeybindManager(tk.Tk):
    def __init__(self):
        super().__init__()

        # Starts keyboard
        self.start_keyboard_listener()

        # Read the config file
        self.config = ConfigParser()
        self.config.read('config.ini')

        # Title
        self.title("Auto Clicker V2.1")
        self.key_in_config = self.config.get('General', 'keybind')

        # Create a label widget and add it to the window
        self.label_text = f"Hello There, Press [{self.key_in_config.upper()}] to start"
        self.label = tk.Label(self, text=self.label_text)
        self.label.pack(pady=10)

        # Status label and coordinates
        self.cord_x = self.config.get('General', 'coordinates_x')
        self.cord_y = self.config.get('General', 'coordinates_Y')
        self.location_message = f"X={self.cord_x} Y={self.cord_y}"
        self.location = f"{self.location_message}"
        self.status_label = tk.Label(self, text=f"Coordinates: {self.location}", font=('Arial', 12, 'bold'))
        self.status_label.pack()

        # Change keybind
        self.keybind_button = tk.Button(text="Change keybind", width=50, command=self.change_keybind)
        self.keybind_button.pack(pady=10)

        # Change coordinates
        self.coordinates_button = tk.Button(text="Change coordinates", width=50, command=self.change_coordinates)
        self.coordinates_button.pack(pady=10)

    # For starting the keyboard listener using a different thread
    @staticmethod
    def start_keyboard_listener():
        # Create a thread for running the keyboard listener
        keyboard_listener_thread = threading.Thread(target=key_start)
        keyboard_listener_thread.daemon = True
        keyboard_listener_thread.start()

    def change_keybind(self):
        new_key = keyboard.read_key()  # Ask for key
        # Change the keybind in the config
        self.config.set('General', 'keybind', new_key)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        # Notify the user to restart program
        self.status_label.config(text=f"Status: {self.location} | Restart Program To Save Changes")

    def change_coordinates(self):
        self.status_label.config(text="Capturing Coordinates In 5 Seconds")
        self.after(5000, self.capture_coordinates)

    def capture_coordinates(self):
        # Get the X,Y and save changes to the config file
        new_x, new_y = coordinate_get()
        self.config.set('General', 'coordinates_x', str(new_x))
        self.config.set('General', 'coordinates_y', str(new_y))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        # Notify user to restart program
        self.location = f"Coordinates: X={str(new_x)} Y={str(new_y)} | Restart Program To Save Changes"
        self.status_label.config(text=f"{self.location}")


def main():
    app = CustomKeybindManager()
    app.mainloop()


if __name__ == "__main__":
    main()
