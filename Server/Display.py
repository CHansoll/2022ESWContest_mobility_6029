from tkinter import *
import tkinter as tk
import tkinter.font
import time
import os


# return Warning statement for each situation
def switch(str):
    switcher = {
        'uphill': 'Incorrect driving on an uphill road is adversely affecting the battery.\n\n Please drive carefully.',
        'downhill': 'Incorrect driving on an downhill road is adversely affecting the battery.\n\n Please drive carefully.',
        'bump': 'Incorrect driving on a speed bump has a bad effect on the battery.\n\n Please drive carefully.',
        'winter': 'The low ambient temperature is adversely affecting the battery.\n\n Please drive carefully.',
        'overcharge': 'Overcharge is adversely affecting the battery.\n\n Please be careful.',
        'overdischarge': 'Overdischarge is adversely affecting the battery.\n\n Please be careful.',
        'overcurrent': 'Overcurrent is adversely affecting the battery.\n\n Please be careful.'}
    return switcher.get(str, 'ooo')


# Function that floats the warning window for each situation
def allinone(str):
    root = tk.Tk()
    root.geometry('800x600')
    root.title("Warning!")

    font = tkinter.font.Font(size=10)

    button = tk.Button(root, text="okay", width=30, height=2, font=10, command=root.destroy)
    button.pack(side="bottom")
    button.pack()

    label = tk.Label(root, text=switch(str), width=800, height=80, font=font)
    label.pack(side="top")
    root.after(1000, lambda: root.destroy())
    if switch(str) == 'ooo':
        time.sleep(0.1)
    else:
        root.mainloop()