import tkinter as tk


class Base:
    def __init__(self, master):
        self._master = master
        
        self._frame = tk.Frame(self._master)

    @property
    def frame(self):
        return self._frame
    
    def on_exception(self, exc: Exception):
        pass