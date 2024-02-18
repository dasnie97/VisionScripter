import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter import font
from src.Helpers import InputConverter, SequenceCreator, Executor
from pynput.keyboard import Listener as KeyboardListener
import tkinter.messagebox
import tkinter.scrolledtext as scrolledtext
import threading

class MainWindow:
    def __init__(self) -> None:
        self.inputConverter = InputConverter()
        self.sequenceCreator = SequenceCreator()
        self.executor = Executor()
        self.run_automatically = False
        self.setup_window()

    def setup_window(self):
        keyboard_listener = KeyboardListener(on_press=self.key_press)
        keyboard_listener.start()

        root = tk.Tk()
        self.configure_window_basis(root)
        self.configure_window_widgets(root)
        root.mainloop()

    def configure_window_basis(self, root):
        root.title("AutoClicker v1.0")

        root.call('wm', 'attributes', '.', '-topmost', '1')

        screen_ratio = 37.79 / root.winfo_fpixels('1c')
        default_font_size = int(screen_ratio * 10)

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=default_font_size)
        root.option_add("*Font", default_font)

        window_width = 310
        window_height = 200

        # get the screen dimension
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        right_x = int(screen_width - 1.5 * window_width)
        down_y = int(screen_height - 1.5 * window_height)

        # set the position of the window to the center of the screen
        root.geometry(f'{window_width}x{window_height}+{right_x}+{down_y}')
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

        currentRecordFrame = ttk.Frame(root, borderwidth=1, width=80, height=80)
        currentRecordFrame.grid_propagate(0)
        currentRecordFrame.columnconfigure(0, weight=1)
        currentRecordFrame.rowconfigure(0, weight=1)
        currentRecordFrame.rowconfigure(1, weight=1)
        currentRecordFrame.rowconfigure(2, weight=1)
        self.nameAndSurnameLabel = ttk.Label(currentRecordFrame, text="")
        self.nameAndSurnameLabel.grid(row=0, column=0)
        self.entryTimeLabel = ttk.Label(currentRecordFrame, text="")
        self.entryTimeLabel.grid(row=1, column=0)
        self.exitTimeLabel = ttk.Label(currentRecordFrame, text="")
        self.exitTimeLabel.grid(row=2, column=0)
        currentRecordFrame.grid(column=5, row=1)

        recordNavigationFrame = ttk.Frame(root, borderwidth=1, width=70, height=30)
        recordNavigationFrame.grid_propagate(0)
        recordNavigationFrame.columnconfigure(0, weight=1)
        recordNavigationFrame.columnconfigure(1, weight=1)
        recordNavigationFrame.rowconfigure(0, weight=1)
        self.nextRecordButton = ttk.Button(recordNavigationFrame, text=">", command=self.next_record_button_click)
        self.nextRecordButton.grid(row=0, column=1)
        self.nextRecordButton["state"] = tk.DISABLED
        self.prevRecordButton = ttk.Button(recordNavigationFrame, text="<", command=self.prev_record_button_click)
        self.prevRecordButton.grid(row=0, column=0)
        self.prevRecordButton["state"] = tk.DISABLED
        recordNavigationFrame.grid(column=5, row=0)

        self.input_file_text = scrolledtext.ScrolledText(root, height=7, width=13)
        self.input_file_text.grid(column=0, row=1, sticky=tk.EW, padx=3, pady=5, columnspan=4, rowspan=3)
        self.input_file_text.tag_configure('highlightline', background='yellow')
        self.input_file_text["state"] = tk.DISABLED
        
        self.status_label = ttk.Label(root, text="")
        self.status_label.grid(column=5, row=0, sticky=tk.NE, padx=5, pady=5)

        record_to_be_inserted_label = ttk.Label(root, text="")
        record_to_be_inserted_label.grid(column=5, row=1, padx=5, pady=5)

        self.insert_record_button = ttk.Button(root, text="Wpisz (F2)", command=self.key_press('f2'))
        self.insert_record_button.grid(column=0, row=4, sticky=tk.EW, padx=5, pady=5)
        self.insert_record_button["state"] = tk.DISABLED

        self.auto_run_button = ttk.Button(root, text="Auto (F8)", command=self.key_press('f8'))
        self.auto_run_button.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)
        self.auto_run_button["state"] = tk.DISABLED

        finish_button = ttk.Button(root, text="Zakończ", command=self.stop_sequence_button_click)
        finish_button.grid(column=5, row=4, sticky=tk.EW, padx=5, pady=5)

        choose_file_button = ttk.Button(root, text="Wybierz plik", command=self.choose_file_button_click)
        choose_file_button.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        
        self.learn_sequence_button = ttk.Button(root, text="Naucz sekwencji", command=self.learn_sequence_button_click)
        self.learn_sequence_button.grid(column=1, row=0, sticky=tk.NW, padx=5, pady=5)
        self.learn_sequence_button["state"] = tk.DISABLED

    def next_record_button_click(self):
        try:
            self.executor.move_to_next_sequence()
            self.input_file_text.see(f"{self.executor.external_iterator + 3}.end")
            self.input_file_text.tag_remove('highlightline', '1.0', 'end')
            self.input_file_text.tag_add('highlightline', f"{self.executor.external_iterator+1}.0", f"{self.executor.external_iterator+2}.0")
            self.set_data_to_write_labels(self.executor.external_iterator)
        except Exception as e:
            if type(e) is IndexError:
                tkinter.messagebox.showinfo('Koniec danych', 'Nie ma więcej obecności do wpisania.')
            else:
                tkinter.messagebox.showinfo('Błąd', 'Wystąpił błąd.')

    def prev_record_button_click(self):
        self.executor.move_to_prev_sequence()
        self.input_file_text.see(f"{self.executor.external_iterator}.end")
        self.input_file_text.tag_remove('highlightline', '1.0', 'end')
        self.input_file_text.tag_add('highlightline', f"{self.executor.external_iterator+1}.0", f"{self.executor.external_iterator+2}.0")
        self.set_data_to_write_labels(self.executor.external_iterator)

    def choose_file_button_click(self):
        chosen_file = askopenfile()
        if chosen_file == None:
            return
        try:
            self.inputConverter.Convert(chosen_file.name)
            self.read_file_and_write_to_textbox(chosen_file.name)
            self.executor.reset()
            self.set_data_to_write_labels(self.executor.external_iterator)
            if self.sequenceCreator.sequence_exists():
                self.sequenceCreator.CreateSequence(self.inputConverter.converted)
                self.executor.load_sequences(self.sequenceCreator.sequence)
        except Exception as e:
            if type(e) is ValueError:
                tkinter.messagebox.showerror('Błąd',f"{str(e)}")
            else:
                tkinter.messagebox.showerror('Błąd', 'Nieprawidłowy plik!')

    def read_file_and_write_to_textbox(self, file_path):
        self.input_file_text["state"] = tk.NORMAL
        self.input_file_text.delete('1.0', 'end')
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                self.input_file_text.insert(tkinter.END, line)
        self.input_file_text.tag_add('highlightline', '1.0', '2.0')
        self.input_file_text["state"] = tk.DISABLED
        self.learn_sequence_button["state"] = tk.NORMAL

    def set_data_to_write_labels(self, index):
        self.nameAndSurnameLabel.config(text=self.inputConverter.converted[index].name + "\n" + self.inputConverter.converted[index].surname)
        self.entryTimeLabel.config(text=self.inputConverter.converted[index].entry_time)
        self.exitTimeLabel.config(text=self.inputConverter.converted[index].exit_time)

    def learn_sequence_button_click(self):
        tkinter.messagebox.showinfo('Rozpocznij uczenie sekwencji','Wciśnij F2 aby rozpocząć uczenie sekwencji. Wciśnij ponownie F2 gdy skończysz.')

    def insert_record_button_click(self):
        try:
            self.executor.execute_next_step()
            self.input_file_text.see(f"{self.executor.external_iterator + 3}.end")
            self.input_file_text.tag_remove('highlightline', '1.0', 'end')
            self.input_file_text.tag_add('highlightline', f"{self.executor.external_iterator+1}.0", f"{self.executor.external_iterator+2}.0")
            self.set_data_to_write_labels(self.executor.external_iterator)
        except Exception as e:
            if type(e) is IndexError:
                tkinter.messagebox.showinfo('Koniec danych', 'Nie ma więcej obecności do wpisania.')
            else:
                tkinter.messagebox.showinfo('Błąd', 'Wystąpił błąd.')
    
    def stop_sequence_button_click(self):
        sys.exit()
    
    def key_press(self, key):
        try:
            if key.name == 'f2':
                if self.sequenceCreator.sequence_exists():
                    self.insert_record_button_click()
                else:
                    self.record_sequence()
            if key.name == 'f8':
                if self.run_automatically == True:
                    self.run_automatically = False
                    self.auto_run_button["text"] = "Auto (F8)"
                else:
                    self.run_automatically = True
                    self.auto_run_button["text"] = "Stop"
                    threading.Thread(target=self.auto_clicker).start()
            if key.name == 'right':
                self.next_record_button_click()
            if key.name == 'left':
                self.prev_record_button_click()
        except AttributeError:
            pass

    def record_sequence(self):
        self.sequenceCreator.RecordActions()
        self.sequenceCreator.CreateSequence(self.inputConverter.converted) #TODO reuse existing sequence for new input files
        self.executor.load_sequences(self.sequenceCreator.sequence)
        self.insert_record_button.configure(state=tk.NORMAL)
        self.auto_run_button.configure(state=tk.NORMAL)
        self.executor.move_to_next_sequence()
        self.set_data_to_write_labels(self.executor.external_iterator)
        self.nextRecordButton["state"] = tk.NORMAL
        self.prevRecordButton["state"] = tk.NORMAL

    def auto_clicker(self):
        while self.run_automatically:
            self.insert_record_button_click()
            time.sleep(0.15)
            if self.executor.external_limit_reached():
                self.auto_run_button["text"] = "Auto (F8)"
                self.run_automatically = False
                break