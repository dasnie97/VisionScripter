import time
import pyautogui
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Controller

stepOver = False

def RepeatAction(sequence):

    delay = 0.01
    global stepOver
    keyboard_listener = KeyboardListener(on_press=on_press)
    keyboard_listener.start()

    for action in sequence:
        stepOver = False
        while stepOver == False:
            time.sleep(delay)
            pass
        if isinstance(action, tuple):
            pyautogui.moveTo(*action)
            time.sleep(delay)
            pyautogui.click(clicks=3)
            time.sleep(delay)
        if isinstance(action, str):
            time.sleep(delay)
            Controller().type(action)
            time.sleep(delay)
            pyautogui.press('enter')
            time.sleep(delay)
    print("Koniec!")

    keyboard_listener.stop()
    keyboard_listener.join()


def on_press(key):
    global stepOver
    try:
        if key.name == 'f2':
            stepOver = True
        if key.name == 'esc':
            quit()
    except AttributeError:
        pass

