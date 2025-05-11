import tkinter as tk
from tkinter import font

from events.data import FontSizeChangedData
from events.events import Event
from events.listener import EventListener
from enums.enums import EventType


class Settings(EventListener):
    def __init__(self):
        self.frame = tk.Frame()

        self.font_var = tk.IntVar(value=10)
        self.color_var = tk.StringVar(value="green")

        self.title = tk.Label(self.frame, text="設定", font=font.Font(family='Arial', size=28))
        self.title.pack(pady=(10, 5))

        self.font_size_label = tk.Label(self.frame, text="字體大小")
        self.font_size_label.pack(ipadx=5, ipady=5)

        self.font_size_scrollbar = tk.Scale(
            self.frame,
            from_=self.font_var.get(),
            to=14,
            orient="horizontal",
            command=self.on_fs_changed,
            variable=self.font_var
        )
        self.font_size_scrollbar.pack(ipadx=5, ipady=5, fill="x", padx=10)

        self.font_size_show_label = tk.Label(self.frame, text=str(self.font_var.get()))
        self.font_size_show_label.pack()

    def on_fs_changed(self, _):
        fs = self.font_var.get()
        data = FontSizeChangedData(fs)
        event = Event(EventType.FS_CHANGED, data)
        event.emit()
        self.font_size_label.configure(font=font.Font(size=fs))
        self.font_size_show_label.configure(text=str(fs), font=font.Font(size=fs))