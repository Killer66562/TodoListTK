import tkinter as tk
from tkinter import ttk
from .base import Base

class SettingsFrame(Base):
    def __init__(self, master):
        super().__init__(master)

        label = ttk.Label(self.frame, text="設定", font=("Arial", 16))
        label.pack(pady=20)

        self.light_btn = ttk.Button(self.frame, text="亮色主題", command=lambda: ttk.Style().theme_use("default"))
        self.dark_btn = ttk.Button(self.frame, text="暗色主題", command=lambda: ttk.Style().theme_use("clam"))

        self.light_btn.pack(pady=5)
        self.dark_btn.pack(pady=5)