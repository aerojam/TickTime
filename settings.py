import json
import os
from pathlib import Path

class Settings:
    def __init__(self, window_name):
        self.data = {}
        if os.name == 'nt':
            self.settings_dir = Path.home() / os.getenv('APPDATA') / 'ticktime'
        else:
            self.settings_dir = Path.home() / '.config' / 'ticktime'
        self.settings_file = self.settings_dir / f'{window_name}.json'
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