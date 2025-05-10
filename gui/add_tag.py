import tkinter as tk
from tkinter import messagebox

from enums.enums import EventType
from events.data import EventData
from events.listener import EventListener


class AddTag(EventListener):
    def __init__(self, master):
        super().__init__()
        self.tag_var = tk.StringVar(value="")

        self.window = tk.Toplevel(master)
        self.window.title("新增標籤")
        self.window.minsize(400, 40)
        self.window.maxsize(400, 40)

        self.frame = tk.Frame(self.window)
        self.frame.pack(fill="both")

        self.entry = tk.Entry(self.frame, textvariable=self.tag_var)
        self.entry.pack(side="left", expand=True, fill="x")

        self.btn = tk.Button(self.frame, text="新增", command=self.on_btn_clicked)
        self.btn.pack(side="right")

    def on_btn_clicked(self):
        tag = self.tag_var.get()
        if not tag:
            messagebox.showwarning("警告", "請輸入標籤", parent=self.window)
        else:
            print(tag)