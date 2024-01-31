import time
import keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from src.Models.Presence import Presence
import pyautogui
from pynput.keyboard import Controller

class SequenceCreator:
    def __init__(self) -> None:
        self.word = ""
        self.sequence = []

    def CreateSequence(self, presence_list:list):
        self.RecordActions()
        parsed_sequence = []
        for presence in presence_list:
            counter = 0
            sequence_step = []
            for step in self.sequence:
                if isinstance(step, str):
                    if counter == 0:
                        sequence_step.append(presence.surname + " " + presence.name)
                    elif counter == 1:
                        sequence_step.append(presence.entry_time)
                    elif counter == 2:
                        sequence_step.append(presence.exit_time)
                    counter += 1
                else:
                    sequence_step.append(step)
            parsed_sequence.append(sequence_step)
        self.sequence = parsed_sequence

    def RecordActions(self):
        mouse_listener = MouseListener(on_click=self.on_click)
        mouse_listener.start()
        keyboard_listener = KeyboardListener(on_press=self.on_press)
        keyboard_listener.start()

        try:
            while True:
                time.sleep(0.01)
                if keyboard.is_pressed('f2'):
                    break

        except KeyboardInterrupt:
            pass

        finally:
            mouse_listener.stop()
            mouse_listener.join()
            keyboard_listener.stop()
            keyboard_listener.join()
        
    def on_click(self, x, y, button, pressed):
        if pressed == True:
            self.append_text_input(self.word)
            self.word = ""
            self.sequence.append((x,y))

    def append_text_input(self, text):
        if text != "":
            self.sequence.append(text)

    def on_press(self, key):
        try:
            self.word += key.char
        except AttributeError:
            if key.name == 'space':
                self.word += ' '

class InputConverter:
    def __init__(self) -> None:
        self.converted = []

    def Convert(self, path):
        self.converted.clear()
        with open(path, encoding="utf-8") as f:
            for line in f:
                self.AppendRecord(line)

    def AppendRecord(self, line:str):
        line = line.strip()
        splitted = line.split(' ')
        exitTime = splitted[3]
        exitTime = exitTime.replace('.', ':')
        exitTime = self.AssureProperTimeFormat(exitTime)
        entryTime = splitted[2]
        entryTime = entryTime.replace('.', ':')
        entryTime = self.AssureProperTimeFormat(entryTime)
        name = splitted[0].capitalize().strip()
        surname = splitted[1].capitalize().strip()
        presence = Presence(name, surname, entryTime, exitTime)
        self.converted.append(presence)

    def AssureProperTimeFormat(self, timeString):
        splitted = timeString.split(':')
        if len(splitted[0]) == 1:
            timeString = self.insert_char(timeString, '0', 0)
        return timeString

    def insert_char(self, string, char, index):
        return string[:index] + char + string[index:]
    
class Executor:
    def __init__(self) -> None:
        self.internal_iterator = 0
        self.external_iterator = 0

    def step_over(self, sequence):
        #TODO: check if iterators reached limits

    def execute_step(self, sequence):
        delay = 0.01
        if isinstance(sequence[self.external_iterator][self.internal_iterator], tuple):
            pyautogui.moveTo(*sequence[self.external_iterator][self.internal_iterator])
            time.sleep(delay)
            pyautogui.click(clicks=3)
            time.sleep(delay)
        if isinstance(sequence[self.external_iterator][self.internal_iterator], str):
            time.sleep(delay)
            Controller().type(sequence[self.external_iterator][self.internal_iterator])
            time.sleep(delay)
            pyautogui.press('enter')
            time.sleep(delay)
