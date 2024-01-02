import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile

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

tk.Label(root, text='Classic Label').pack()
ttk.Label(root, text='Themed Label').pack()

root.mainloop()