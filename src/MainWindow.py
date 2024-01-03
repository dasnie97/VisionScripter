import tkinter as tk
from tkinter import END, ttk
from tkinter.filedialog import askopenfile
from tkinter.font import Font
from InputConverter import *
from pynput.keyboard import Listener as KeyboardListener

class MainWindow:
    def __init__(self) -> None:
        self.counter = 0
        self.setup_window()
    
    def setup_window(self):
        root = tk.Tk()
        root.title("AutoClicker")

        window_width = 300
        window_height = 200

        # get the screen dimension
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        root.resizable(False, False)
        root.iconbitmap('./assets/P.ico')

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.columnconfigure(3, weight=1)
        root.columnconfigure(4, weight=1)
        root.columnconfigure(5, weight=1)

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)

        s = ttk.Style()
        s.configure('TFrame', background='green')

        frame = ttk.Frame(root, width=100, height=50)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        self.nameAndSurnameLabel = ttk.Label(frame, text="")
        self.nameAndSurnameLabel.grid(row=0, column=0)
        self.entryTimeLabel = ttk.Label(frame, text="")
        self.entryTimeLabel.grid(row=1, column=0)
        self.exitTimeLabel = ttk.Label(frame, text="")
        self.exitTimeLabel.grid(row=2, column=0)
        frame.grid(column=5, row=2, sticky=tk.N)

        self.input_file_text = tk.Text(root, height=7, width=10)
        self.input_file_text.grid(column=0, row=1, sticky=tk.EW, padx=5, pady=5, columnspan=3, rowspan=3)
        myFont = Font(family="Times New Roman", size=10)
        self.input_file_text.configure(font=myFont)
        
        ttk.Label(root, text="Status").grid(column=5, row=0, sticky=tk.NE, padx=5, pady=5)
        ttk.Label(root, text="Do wpisania:").grid(column=5, row=1, padx=5, pady=5)
        ttk.Button(root, text="Wpisz (F2)", command=self.insert_record).grid(column=0, row=4, sticky=tk.EW, padx=5, pady=5)
        ttk.Button(root, text="Zakończ (F8)", command=self.stop_sequence).grid(column=5, row=4, sticky=tk.EW, padx=5, pady=5)
        ttk.Button(root, text="Wybierz plik", command=self.choose_file).grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        ttk.Button(root, text="Naucz sekwencji", command=self.stop_sequence).grid(column=1, row=0, sticky=tk.NW, padx=5, pady=5)

        keyboard_listener = KeyboardListener(on_press=self.key_press)
        keyboard_listener.start()

        root.mainloop()

        keyboard_listener.stop()
        keyboard_listener.join()

    def choose_file(self):
        file = askopenfile()
        with open(file.name, encoding="utf-8") as f:
            for line in f:
                self.input_file_text.insert(END, line.strip() + "\n")
        Convert(file.name)
        self.set_data_to_write_labels(0)
        
    def set_data_to_write_labels(self, index):
        self.nameAndSurnameLabel.config(text=converted[index][0].replace(" ", "\n"))
        self.entryTimeLabel.config(text=converted[index][1])
        self.exitTimeLabel.config(text=converted[index][2])

    def learn_sequence():
        file = askopenfile()
        return file

    def insert_record(self):
        self.counter += 1
        self.set_data_to_write_labels(self.counter)

    def stop_sequence():
        file = askopenfile()
        return file
    
    def key_press(self, key):
        try:
            if key.name == 'f2':
                self.counter += 1
                self.set_data_to_write_labels(self.counter)
        except AttributeError:
            pass


test = MainWindow()

#TODO: cleanup and set events