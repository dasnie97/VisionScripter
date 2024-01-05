import time
import keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from Models.Presence import Presence

class SequenceCreator:
    def __init__(self) -> None:
        self.word = ""
        self.sequence = []

    def CreateSequence(self, input:list):
        self.RecordActions()
        newList = []
        for item in input:
            counter = 0
            for step in self.sequence:
                if isinstance(step, str):
                    newList.append(item[counter])
                    counter += 1
                else:
                    newList.append(step)
        return newList

    def RecordActions(self):
        print("Zacznij ruszać kursorem, klikać i wpisywać tekst. Czynności będą nagrywane, a potem odtworzone. Gdy skończysz cykl wciśnij f2.")
        mouse_listener = MouseListener(on_click=self.on_click)
        mouse_listener.start()
        keyboard_listener = KeyboardListener(on_press=self.on_press)
        keyboard_listener.start()

        try:
            while True:
                if keyboard.is_pressed('f2'):
                    time.sleep(0.3)
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
    