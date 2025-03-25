import time
import tkinter as tk
from tkinter import ttk
from tkinter import font
from settings import Settings

class SmartWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.settings = Settings(self.__class__.__name__)
        self.root.title(self.settings.get("title"))
        self.root.geometry(self.settings.get('geometry'))
        self.settings.set('fullscreen', False)
        self.bind_events()
        self.label = ttk.Label(self.root, text="F to fullscreen, +/- to scale", font="TkDefaultFont")
        self.label.pack(pady=(20, 0))
        self.current_time_string = ''
        self.custom_display_font = font.Font(family=font.nametofont("TkFixedFont").actual("family"))
        self.clock_label = ttk.Label(self.root, text=self.current_time_string, font=self.custom_display_font, padding=(5, 10))
        self.clock_label.pack(expand=True)
        self.update_font_size()
        self.root.grab_set()

    #
    # Don't use this method -- bad approach:
    #
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

    def update_font_size(self, event=None):
        new_font = font.Font(family=font.nametofont("TkFixedFont").actual("family"), size=24)
        new_font_size = int(new_font.cget("size") * self.settings.get('scale'))
        new_font.config(size=max(new_font_size, 6))
        self.clock_label.config(font=new_font)
        self.settings.set('scale', self.settings.get('scale'))

    def update_geometry(self, event):
        #self.update_font_size()
        #self.set_font_size_to_fit_window()
        if not self.settings.get('fullscreen'):
            self.settings.set('geometry', self.root.geometry())

    def increase_font_size(self, event=None):
        self.settings.set('scale', self.settings.get('scale') + 0.5)
        self.update_font_size()
        #self.set_font_size_to_fit_window()

    def decrease_font_size(self, event=None):
        self.settings.set('scale', max(self.settings.get('scale') - 0.5, 0.1))
        self.update_font_size()
        #self.set_font_size_to_fit_window()

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
