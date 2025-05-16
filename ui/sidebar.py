import tkinter as tk
import os

from tkinter import ttk
from tkinter import messagebox
from typing import Callable
from PIL import Image, ImageTk

from models import local
from models.local import Tag
from ui.tag import TagButton

from .base import Base

class SideBar(Base):
    def __init__(
        self, master, 
        on_add_tag_btn_clicked_cb: Callable[[str], None], 
        on_all_btn_clicked_cb: Callable[[], None], 
        on_today_btn_clicked_cb: Callable[[], None]
    ):
        super().__init__(master)
        self._filter = None

        self._tag_var = tk.StringVar(value="")

        self._frame_open = True

        self.top_frame = ttk.Frame(self.frame)
        self.top_frame.pack(side="top")

        self.bottom_frame = ttk.Frame(self.frame)
        self.bottom_frame.pack(side="bottom", expand=True, fill="both")

        # 圖片路徑設定
        assets_path = os.path.join("assets")

        open_icon_image = Image.open(os.path.join(assets_path, "icon-open.png"))
        open_icon_image = open_icon_image.resize((30, 30))
        self.open_icon = ImageTk.PhotoImage(open_icon_image)

        close_icon_image = Image.open(os.path.join(assets_path, "icon-close.png"))
        close_icon_image = close_icon_image.resize((30, 30))
        self.close_icon = ImageTk.PhotoImage(close_icon_image)

        # 開關按鈕
        self.toggle_button = ttk.Button(self.frame, text="", image=self.close_icon, command=self.toggle)
        self.toggle_button.pack(pady=(10, 5), padx=10, anchor="w")

        self.title_label = ttk.Label(self.bottom_frame, text="TodoList", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.index_btn = ttk.Button(self.bottom_frame, text="全部", command=self.on_all_btn_clicked)
        self.index_btn.pack(fill="x", pady=5, padx=10)

        self.today_btn = ttk.Button(self.bottom_frame, text="今天", command=self.on_today_btn_clicked)
        self.today_btn.pack(fill="x", pady=5, padx=10)
            
        # 行事曆按鈕
        self.calendar_button = ttk.Button(
            self.bottom_frame,
            text="行事曆"
        )
        self.calendar_button.pack(pady=10, padx=10, fill="x")
        
        # 任務統計按鈕
        self.stats_button = ttk.Button(
            self.bottom_frame,
            text="任務統計"
        )
        self.stats_button.pack(pady=(0, 10), padx=10, fill="x")


        self.my_items_label = ttk.Label(self.bottom_frame, text="─ 我的項目 ─")
        self.my_items_label.pack(pady=10)

        self._tag_btns: list[TagButton] = []

        self.tag_name_label = ttk.Label(self.bottom_frame, text="標籤名稱")
        self.tag_name_label.pack(anchor="w", pady=2, padx=20)

        self.tag_name_entry = ttk.Entry(self.bottom_frame, textvariable=self._tag_var)
        self.tag_name_entry.pack(fill="x", pady=2, padx=20)

        self.tag_add_btn = ttk.Button(self.bottom_frame, text="新增標籤", command=self.on_add_tag_btn_clicked)
        self.tag_add_btn.pack(fill="x", pady=2, padx=20)

        # 設定按鈕
        self.settings_button = ttk.Button(
            self.bottom_frame,
            text="設定",
        )
        self.settings_button.pack(side="bottom", pady=10, padx=10, fill="x")

        self.on_add_tag_btn_clicked_cb = on_add_tag_btn_clicked_cb
        self.on_all_btn_clicked_cb = on_all_btn_clicked_cb
        self.on_today_btn_clicked_cb = on_today_btn_clicked_cb

    def on_add_tag_btn_clicked(self):
        tag_name = self._tag_var.get()
        if not tag_name:
            messagebox.showwarning(title="警告", message="請輸入標籤名稱")
            return
        self.on_add_tag_btn_clicked_cb(tag_name)
        self._tag_var.set("")

    def toggle(self):
        if self._frame_open:
            self.frame.configure(width=70)
            self.bottom_frame.pack_forget()
            self.toggle_button.configure(image=self.open_icon)
            self._frame_open = False
        else:
            self.bottom_frame.pack(fill="both", expand=True)
            self.frame.configure(width=200)
            self.toggle_button.configure(image=self.close_icon)
            self._frame_open = True

    def set_tag_btns(self, tags: list[Tag], main_btn_cb: Callable[[str], None], delete_btn_cb):
        for tag_btn in self._tag_btns:
            tag_btn.frame.pack_forget()
        self._tag_btns.clear()
        for tag in tags:
            self._tag_btns.append(TagButton(self.bottom_frame, tag.name, main_btn_cb, delete_btn_cb))
        for tag_btn in self._tag_btns:
            tag_btn.frame.pack(fill="x", pady=2, padx=20)

    def on_all_btn_clicked(self):
        self._filter = "all"
        self.on_all_btn_clicked_cb()

    def on_today_btn_clicked(self):
        self._filter = "today"
        self.on_today_btn_clicked_cb()

    def get_filter(self) -> str:
        return self._filter
    
    def reset_filter(self):
        self._filter = None
        

if __name__ == "__main__":
    window = tk.Tk()

    sidebar = SideBar(window)
    sidebar.frame.pack(fill="y", side="left")

    window.mainloop()