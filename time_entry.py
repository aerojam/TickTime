import time
import tkinter as tk
from tkinter import ttk
from count_down import CountDown

class TimeEntry:
    def __init__(self, time_entry, prompt="Enter time", title="Time"):
        self.root = tk.Toplevel()
        self.root.title(title)
        
        label = ttk.Label(self.root, text=prompt)
        label.pack(pady=10)
        
        self.time_entry = ttk.Entry(self.root)
        self.time_entry.pack(pady=10)
        
        set_button = ttk.Button(self.root, text="OK", command=self.dismiss)
        set_button.pack(pady=10)

        cancel_button = ttk.Button(self.root, text="Cancel", command=self.dismiss)
        cancel_button.pack()
        
        self.root.protocol("WM_DELETE_WINDOW", self.dismiss) # intercept close button
        self.root.wait_visibility() # can't grab until window appears, so we wait
        self.root.grab_set()        # ensure all input goes to our window
        self.root.wait_window()     # block until window is destroyed

    def dismiss(self):
        self.root.grab_release()
        self.root.destroy()

    def ok_pressed(self):
        count_down_window = CountDown()