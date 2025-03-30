from datetime import datetime, timedelta
import time
import re
import tkinter as tk
from tkinter import ttk
from count_down import CountDown

class TimeEntry:
    def __init__(self, time_entry, prompt="Enter time", title="Time"):
        self.root = tk.Toplevel()
        self.root.title(title)

        self.icon_image = tk.PhotoImage(file='question_icon.png')
        dialog_icon = ttk.Label(self.root, image=self.icon_image)
        dialog_icon.grid(column=0, row=0)
        
        label = ttk.Label(self.root, text=prompt)
        label.grid(column=1, row=0, columnspan=2, sticky=(tk.E, tk.W))
        #label.pack(pady=10)
        
        self.time_entry = ttk.Entry(self.root)
        self.time_entry.grid(column=1, row=1, columnspan=2, sticky=(tk.E, tk.W))
        #self.time_entry.pack(pady=10)
        
        set_button = ttk.Button(self.root, text="OK", command=self.ok_pressed)
        set_button.grid(column=1, row=2, sticky=tk.E)
        #set_button.pack(pady=10)

        cancel_button = ttk.Button(self.root, text="Cancel", command=self.dismiss)
        cancel_button.grid(column=2, row=2, sticky=tk.E)
        #cancel_button.pack()

        #self.root.grid_columnconfigure(1, weight=1)
        #self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.dismiss) # intercept close button
        self.root.wait_visibility() # can't grab until window appears, so we wait
        self.root.grab_set()        # ensure all input goes to our window
        self.root.wait_window()     # block until window is destroyed

    def dismiss(self):
        self.root.grab_release()
        self.root.destroy()

    def ok_pressed(self):
        time_text = self.time_entry.get()
        hours, minutes, seconds = 0, 0, 0
        hours_match   = re.search(r'(\d+)h', time_text)
        minutes_match = re.search(r'(\d+)m', time_text)
        seconds_match = re.search(r'(\d+)s', time_text)
        if hours_match:
            hours = int(hours_match.group(1))
        if minutes_match:
            minutes = int(minutes_match.group(1))
        if seconds_match:
            seconds = int(seconds_match.group(1))
        time_addin = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        if hours == 0 and minutes == 0 and seconds == 0:
            pass
        else:
            self.root.grab_release()
            self.root.destroy()
            count_down_window = CountDown(time_addin)