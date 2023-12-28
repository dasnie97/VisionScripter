import pyautogui

def RepeatAction(sequence):
    for action in sequence:
        if isinstance(action, tuple):
            pyautogui.moveTo(*action, 0.5)
        