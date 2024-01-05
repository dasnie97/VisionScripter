import tkinter as tk
from tkinter import END, ttk
from tkinter.filedialog import askopenfile
from tkinter.font import Font
from Helpers import InputConverter, SequenceCreator
from pynput.keyboard import Listener as KeyboardListener

from Repeater import execute_step

class MainWindow:
    def __init__(self) -> None:
        self.counter = 0
        self.ready_to_go = False
        self._inputConverter = InputConverter()
        self._sequenceCreator = SequenceCreator()
        self.setup_window()

    def setup_window(self):
        root = tk.Tk()

        self.configure_window_basis(root)
        self.configure_window_widgets(root)

        keyboard_listener = KeyboardListener(on_press=self.key_press)
        keyboard_listener.start()

        root.mainloop()

        keyboard_listener.stop()
        keyboard_listener.join()

    def configure_window_basis(self, root):
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

    def configure_window_widgets(self, root):
        s = ttk.Style()
        s.configure('TFrame', background='green')

        frame = ttk.Frame(root, borderwidth=1, width=90, height=80)
        frame.grid_propagate(0)
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

        frame.grid(column=5, row=1)

        self.input_file_text = tk.Text(root, height=7, width=10)
        self.input_file_text.grid(column=0, row=1, sticky=tk.EW, padx=5, pady=5, columnspan=3, rowspan=3)
        self.input_file_text.configure(font=Font(family="Times New Roman", size=10))
        self.input_file_text["state"] = tk.DISABLED
        
        self.status_label = ttk.Label(root, text="")
        self.status_label.grid(column=5, row=0, sticky=tk.NE, padx=5, pady=5)

        record_to_be_inserted_label = ttk.Label(root, text="")
        record_to_be_inserted_label.grid(column=5, row=1, padx=5, pady=5)

        self.insert_record_button = ttk.Button(root, text="Wpisz (F2)", command=self.insert_record_button_click)
        self.insert_record_button.grid(column=0, row=4, sticky=tk.EW, padx=5, pady=5)
        self.insert_record_button["state"] = tk.DISABLED

        finish_button = ttk.Button(root, text="Zakończ (F8)", command=self.stop_sequence_button_click)
        finish_button.grid(column=5, row=4, sticky=tk.EW, padx=5, pady=5)

        choose_file_button = ttk.Button(root, text="Wybierz plik", command=self.choose_file_button_click)
        choose_file_button.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        
        self.learn_sequence_button = ttk.Button(root, text="Naucz sekwencji", command=self.learn_sequence_button_click)
        self.learn_sequence_button.grid(column=1, row=0, sticky=tk.NW, padx=5, pady=5)
        self.learn_sequence_button["state"] = tk.DISABLED

    def choose_file_button_click(self):
        chosen_file = askopenfile()
        self.read_file_and_write_to_textbox(chosen_file.name)

    def learn_sequence_button_click(self):
        self.status_label.config(text="Test")

    def insert_record_button_click(self):
        self.counter += 1
        self.set_data_to_write_labels(self.counter)

    def stop_sequence_button_click(self):
        file = askopenfile()
        return file
    
    def key_press(self, key):
        try:
            if key.name == 'f2':
                if self.ready_to_go:
                    self.counter += 1
                    self.set_data_to_write_labels(self.counter)
                    self.step_over()
                else:
                    self.record_sequence()
        except AttributeError:
            pass

    def read_file_and_write_to_textbox(self, file_path):
        self.input_file_text["state"] = tk.NORMAL
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                self.input_file_text.insert(END, line)
        self.input_file_text["state"] = tk.DISABLED
        self._inputConverter.Convert(file_path)
        self.set_data_to_write_labels(0)
        self.learn_sequence_button["state"] = tk.NORMAL

    def set_data_to_write_labels(self, index):
        self.nameAndSurnameLabel.config(text=self._inputConverter.converted[index].name + "\n" + self._inputConverter.converted[index].surname)
        self.entryTimeLabel.config(text=self._inputConverter.converted[index].entry_time)
        self.exitTimeLabel.config(text=self._inputConverter.converted[index].exit_time)

    def record_sequence(self):
        self.sequence = self._sequenceCreator.CreateSequence(self._inputConverter.converted)
        self.ready_to_go = True
        self.status_label.config(text="")
            
    def step_over(self):
        execute_step(self.sequence, self.counter)

test = MainWindow()

#TODO: cleanup and set events