import configparser
import os
import pyautogui


def config_create():
    # Get middle part of the screen
    screen_width, screen_height = pyautogui.size()
    middle_x = screen_width // 2
    middle_y = screen_height // 2

    # Define the configuration file path
    config_file_path = 'config.ini'

    # Check if the configuration file exists
    if not os.path.exists(config_file_path):
        # Create a new ConfigParser object
        config = configparser.ConfigParser()

        # Add sections and set default values
        config.add_section('General')
        config.set('General', 'keybind', 'r')
        config.set('General', 'coordinates_X', str(middle_x))
        config.set('General', 'coordinates_Y', str(middle_y))

        # Write the configuration data to the file
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
    else:
        print("already have config")