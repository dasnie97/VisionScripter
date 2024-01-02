import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile

global input_file_text

def choose_file():
    global input_file_text
    file = askopenfile()
    input_file_text.insert('1.0', file.readlines())

def learn_sequence():
    file = askopenfile()
    return file

def insert_record():
    file = askopenfile()
    return file

def stop_sequence():
    file = askopenfile()
    return file

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

input_file_text = tk.Text(root, height=1).grid(column=0, row=0, sticky=tk.EW, padx=5, pady=5)
ttk.Button(root, text="Wybierz plik", command=choose_file).grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)
ttk.Button(root, text="Naucz sekwencję", command=learn_sequence).grid(column=2, row=2, sticky=tk.EW, padx=5, pady=5)
ttk.Button(root, text="Wpisz (F2)", command=insert_record).grid(column=3, row=3, sticky=tk.EW, padx=5, pady=5)
ttk.Button(root, text="Zakończ (F8)", command=stop_sequence).grid(column=4, row=4, sticky=tk.EW, padx=5, pady=5)

root.mainloop()

#TODO: create UI