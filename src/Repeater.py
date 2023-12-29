import pyautogui

def RepeatAction(sequence):
    for action in sequence:
        if isinstance(action, tuple):
            pyautogui.moveTo(*action, 0.3)
            pyautogui.leftClick()
        if isinstance(action, str):
            pyautogui.write(action)
    print("Koniec!")