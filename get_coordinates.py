import pyautogui


def coordinate_get():
    # Get the current mouse cursor position
    x, y = pyautogui.position()

    return x, y