from smartwindow import SmartWindow
import time

class Timer(SmartWindow):
    def __init__(self):
        super().__init__()
        self.update_time()
        self.root.mainloop()

    def update_time_label(self):
        self.current_time_string = time.strftime(self.settings.get('time_format'))
        self.clock_label.configure(text=self.current_time_string)

    def update_time(self):
        self.update_time_label()
        now = time.time()
        next_second = (now // 1 + 1) - now
        self.root.after(int(next_second * 1000), self.update_time)