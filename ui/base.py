from tkinter import ttk

class Base:
    def __init__(self, master):
        self._master = master
        
        self._frame = ttk.Frame(self._master, style="TFrame")

    @property
    def frame(self):
        return self._frame
    
    def on_exception(self, exc: Exception):
        pass