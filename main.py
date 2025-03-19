import tkinter as tk
from clock import Clock

def main():
    root = tk.Tk()
    app = Clock(root)
    root.mainloop()

if __name__ == "__main__":
    main()