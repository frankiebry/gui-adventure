# main.py
from gui import GUI

import tkinter as tk
import ttkbootstrap as ttk

if __name__ == "__main__":
    window = ttk.Window(themename='darkly')
    gui = GUI(window)
    window.mainloop()