import tkinter as tk
import time
import json
import os
from pathlib import Path
from tkinter import ttk
from tkinter import font



class Settings:
    def __init__(self):
        self.data = {}
        if os.name == 'nt':
            self.settings_dir = Path.home() / os.getenv('APPDATA') / 'ticktime'
        else:
            self.settings_dir = Path.home() / '.config' / 'ticktime'
        self.settings_file = self.settings_dir / 'settings.json'
        self.load()

    def get(self, key):
        return self.data[key]
    
    def set(self, key, value):
        self.data[key] = value

    def save(self):
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=None)
        except FileNotFoundError:
            self.settings_dir.mkdir(parents=True, exist_ok=True)

    def load(self):
        try:
            with open(self.settings_file, "r") as f:
                self.data = json.load(f)
        except Exception:
            self.data = {}
            self.set('title', 'TickTime')
            self.set('geometry', '500x300+100+80')
            self.set('fullscreen', False)
            self.set('padding', 40)
            self.set('scale', 1.0)
            self.set('time_format', '%H:%M:%S')



class TickTime:
    def __init__(self, root):
        self.root = root
        self.settings = Settings()
        self.root.title(self.settings.get("title"))
        self.root.geometry(self.settings.get('geometry'))
        self.settings.set('fullscreen', False)
        self.bind_events()
        self.label = ttk.Label(self.root, text="F or ESC to fullscreen, Q to exit, +/- to scale", font="TkDefaultFont")
        self.label.pack(pady=(20, 0))
        self.current_time_string = ''
        self.custom_display_font = font.Font(family=font.nametofont("TkFixedFont").actual("family"))
        self.clock_label = ttk.Label(self.root, text=self.current_time_string, font=self.custom_display_font, padding=(self.settings.get('padding'), 20))
        self.clock_label.pack(expand=True)
        self.update_time()

    def update_time_label(self):
        self.current_time_string = time.strftime(self.settings.get('time_format'))
        self.clock_label.configure(text=self.current_time_string)

    def update_time(self):
        self.update_time_label()
        now = time.time()
        next_second = (now // 1 + 1) - now
        self.root.after(int(next_second * 1000), self.update_time)

    def set_font_size_to_fit_window(self, event=None):
        window_width = self.root.winfo_width() - 2 * self.settings.get('padding')
        font_size = 500
        while font_size > 6:
            new_font = font.Font(family=font.nametofont("TkFixedFont").actual("family"), size=font_size)
            temp_canvas = tk.Canvas(self.root)
            text_width = temp_canvas.create_text(0, 0,  text=self.clock_label["text"], font=new_font, anchor="nw")
            text_width = temp_canvas.bbox(text_width)[2]
            temp_canvas.destroy()
            if text_width < window_width:
                new_font_size = int(new_font.cget("size") * self.settings.get('scale'))
                new_font.config(size=max(new_font_size, 6))
                self.clock_label.config(font=new_font)
                self.settings.set('scale', self.settings.get('scale'))
                break
            else:
                font_size -= 6

    def update_geometry(self, event):
        self.set_font_size_to_fit_window()
        if not self.settings.get('fullscreen'):
            self.settings.set('geometry', self.root.geometry())

    def increase_font_size(self, event=None):
        self.settings.set('scale', min(self.settings.get('scale') + 0.1, 1.0))
        self.set_font_size_to_fit_window()

    def decrease_font_size(self, event=None):
        self.settings.set('scale', max(self.settings.get('scale') - 0.1, 0.1))
        self.set_font_size_to_fit_window()

    def bind_events(self):
        self.root.bind("<plus>", self.increase_font_size)
        self.root.bind("<KP_Add>", self.increase_font_size)
        self.root.bind("<minus>", self.decrease_font_size)
        self.root.bind("<KP_Subtract>", self.decrease_font_size)
        self.root.bind("<f>", self.toggle_fullscreen)
        self.root.bind("<Configure>", self.update_geometry)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.settings.save()
        self.root.destroy()

    def toggle_fullscreen(self, event):
        if self.settings.get('fullscreen'):
            self.settings.set('fullscreen', False)
            self.root.attributes('-fullscreen', False)
            self.root.geometry(self.settings.get('geometry'))
        else:
            self.settings.set('geometry', self.root.geometry())
            self.settings.set('fullscreen', True)
            self.root.attributes('-fullscreen', True)
        


def main():
    root = tk.Tk()
    app = TickTime(root)
    root.mainloop()

if __name__ == "__main__":
    main()