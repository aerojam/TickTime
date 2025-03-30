from smartwindow import SmartWindow
from datetime import timedelta
import time

class CountDown(SmartWindow):
    def __init__(self, time_addin):
        super().__init__()
        self.time_format = self.settings.get('time_format')
        self.running = False
        if isinstance(time_addin, timedelta):  # Check if time_addin is a timedelta
            self.time_addin = int(time_addin.total_seconds())  # Convert to seconds
        else:
            self.time_addin = time_addin
        self.original_time_addin = self.time_addin
        self.current_time_string = time.strftime(self.time_format, time.gmtime(self.time_addin))
        self.clock_label.configure(text=self.current_time_string)
        self.root.bind('<space>', self.toggle_timer)
        self.root.bind('<r>', self.reset_timer)
        self.label.config(text="F to fullscreen, +/- to scale, SPACE to start/stop, R to reset")
        self.update_time_label()

    def update_time_label(self):
        self.current_time_string = time.strftime(self.time_format, time.gmtime(self.time_addin))
        self.clock_label.configure(text=self.current_time_string)

    def update_time(self):
        if self.running:
            self.root.after(1000, self.update_time)
            if self.time_addin >= 0:  # Ensure countdown stops at 0
                self.update_time_label()
                self.time_addin -= 1
            else:
                self.running = False  # Stop the timer when it reaches 0

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running:
            self.update_time()

    def reset_timer(self, event):
        self.running = False
        self.time_addin = self.original_time_addin
        self.update_time_label()