import time
import pyautogui, keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from src.ConfigManager import append_mouse_position, sequence


def on_move(x, y):
    print(x, y)

def on_click(x, y, button, pressed):
    if pressed == True:
        record_mouse_position(x, y)

def on_scroll(x, y, dx, dy):
    print(x, y, dx, dy)

def on_press(key):
    try:
        print(f'Key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

def record_mouse_position(x, y):
    append_mouse_position(x, y)

def RecordActions():
    print("Zacznij ruszać kursorem, klikać i wpisywać tekst. Czynności będą nagrywane, a potem odtworzone. Gdy skończysz cykl wciśnij kombinację ctrl + q.")
    mouse_listener = MouseListener(on_click=on_click)
    mouse_listener.start()
    keyboard_listener = KeyboardListener(on_press=on_press)
    keyboard_listener.start()

    try:
        while True:
            if keyboard.is_pressed('ctrl+q'):
                print("pressed!")
                time.sleep(0.3)
                break

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to gracefully exit the script
        pass

    finally:
        # Stop the listener when the script is interrupted
        mouse_listener.stop()
        mouse_listener.join()
        keyboard_listener.stop()
        keyboard_listener.join()
    
    return sequence

