import tkinter as tk
from tkinter import ttk
from clock import Clock
from timer import Timer
from count_down import CountDown

class MainWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TickTime")
        clock_button = ttk.Button(
            self.root,
            text="Clock",
            command=self.open_clock
        )
        timer_button = ttk.Button(
            self.root,
            text="Timer",
            command=self.open_timer
        )
        count_down_button = ttk.Button(
            self.root,
            text="Count Down",
            command=self.open_count_down
        )
        quit_button = ttk.Button(
            self.root,
            text="Quit",
            command=self.exit_app
        )
        clock_button.pack(padx=20, pady=5)
        timer_button.pack(padx=20, pady=5)
        count_down_button.pack(padx=20, pady=5)
        quit_button.pack(padx=20, pady=5)

    def open_clock(self):
        clock_window = Clock()

    def open_timer(self):
        timer_window = Timer()

    def open_count_down(self):
        count_down_window = CountDown()

    def exit_app(self):
        self.root.destroy()
