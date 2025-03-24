from smartwindow import SmartWindow
import time

class Timer(SmartWindow):
    def __init__(self):
        super().__init__()
        self.running = False
        self.elapsed_time = 0
        self.current_time_string = "00:00:00"
        self.time_format = self.settings.get('time_format')
        self.root.bind('<space>', self.toggle_timer)
        self.root.bind('<r>', self.reset_timer)
        self.label.config(text="F to fullscreen, +/- to scale, SPACE to start/stop, R to reset")
        self.update_time_label()

    def update_time_label(self):
        self.current_time_string = time.strftime(self.time_format, time.gmtime(self.elapsed_time))
        self.clock_label.configure(text=self.current_time_string)

    def update_time(self):
        if self.running:
            self.update_time_label()
            self.root.after(1000, self.update_time)
            self.elapsed_time += 1

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running:
            self.update_time()

    def reset_timer(self, event):
        self.running = False
        self.elapsed_time = 0
        self.update_time_label()