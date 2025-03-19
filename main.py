import tkinter as tk
from clock import Clock
from timer import Timer

def main():
    root = tk.Tk()
    app = Clock(root)
    # app = Timer(root)
    root.mainloop()

if __name__ == "__main__":
    main()