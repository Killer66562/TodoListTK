import tkinter as tk
from tkinter import messagebox

from events.listener import EventListener

from enums.enums import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.models import Tag

class AddTag(EventListener):
    def __init__(self, master):
        super().__init__()
        self.engine = create_engine(DB_URL)
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
            return
        with Session(self.engine) as session:
            tag_model = session.query(Tag).filter(Tag.name == tag).first()
            if tag_model:
                messagebox.showwarning("警告", "標籤已存在", parent=self.window)
                return
            tag_model = Tag(name=tag)
            session.add(tag_model)
            session.commit()
        messagebox.showinfo("成功", "標籤新增成功", parent=self.window)