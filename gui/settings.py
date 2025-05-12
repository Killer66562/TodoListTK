import tkinter as tk
import json

from tkinter import font
from tkinter import messagebox
from tkinter import ttk

from events.data import FontSizeChangedData
from events.events import Event
from events.listener import EventListener
from enums.enums import EventType

from models import settings

class Settings(EventListener):
    def __init__(self, master):
        super().__init__()

        self.frame = tk.Frame(master)
        settings_ = settings.Settings()
        try:
            settings_.load("config.json")
        except FileNotFoundError:
            settings_.save("config.json")

        self.font_var = tk.IntVar(value=settings_.font_size)
        self.dark_mode_var = tk.BooleanVar(value=settings_.dark_mode)
        self.notify_var = tk.BooleanVar(value=settings_.notify)

        self.color_var = tk.StringVar(value="green")

        self.title = tk.Label(self.frame, text="設定", font=font.Font(family='Arial', size=28))
        self.title.pack(pady=(10, 5))

        self.font_size_label = tk.Label(self.frame, text="字體大小")
        self.font_size_label.pack(anchor="w", ipadx=5, ipady=5)

        self.font_size_scrollbar = tk.Scale(
            self.frame,
            from_=10,
            to=14, 
            orient="horizontal",
            command=self.on_scrollbar_scrolled,
            variable=self.font_var
        )
        self.font_size_scrollbar.pack(ipadx=5, ipady=5, fill="x", padx=10)

        self.bottom_frame = tk.Frame(self.frame)
        self.bottom_frame.pack(fill="x")

        self.save_btn = tk.Button(self.bottom_frame, command=self.on_save, text="保存")
        self.save_btn.pack(side="left")

    def on_save(self):
        settings_ = settings.Settings()
        settings_.font_size = self.font_var.get()
        settings_.dark_mode = self.dark_mode_var.get()
        settings_.notify = self.notify_var.get()

        try:
            settings_.save("config.json")
            messagebox.showinfo("成功", "設定保存成功")
        except:
            messagebox.showerror("錯誤", "設定保存失敗")

    def on_scrollbar_scrolled(self, _):
        fs = self.font_var.get()
        style = ttk.Style()