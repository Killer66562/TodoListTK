import tkinter as tk
import os
from tkinter import font

from PIL import Image, ImageTk
from enums.enums import EventType
from events.events import Event
from events.listener import EventListener
from events.data import EventData, FontSizeChangedData, IndexBtnClickedData


class Sidebar(EventListener):
    def __init__(self, master):
        super().__init__()
        self._frame_open = True
        self._components = []

        self.frame = tk.Frame(master, width=200)
        self.frame.pack_propagate(0)
        self.frame.pack()

        self.top_frame = tk.Frame(self.frame)
        self.top_frame.pack(side="top")

        self.bottom_frame = tk.Frame(self.frame)
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
        self.toggle_button = tk.Button(self.frame, text="", image=self.close_icon, command=self.toggle)
        self.toggle_button.pack(pady=(10, 5), padx=10, anchor="w")

        self.title_label = tk.Label(self.bottom_frame, text="TodoList", font=("Arial", 20))
        self.title_label.pack(pady=10)
        self._components.append(self.title_label)

        self.index_btn = btn = tk.Button(self.bottom_frame, text="全部", command=self.on_index_btn_clicked)
        self.index_btn.pack(fill="x", pady=5, padx=10)
        self._components.append(self.index_btn)

        self.today_btn = btn = tk.Button(self.bottom_frame, text="今天", command=self.on_today_btn_clicked)
        self.today_btn.pack(fill="x", pady=5, padx=10)
        self._components.append(self.today_btn)

        self.preview_btn = btn = tk.Button(self.bottom_frame, text="近期", command=self.on_preview_btn_clicked)
        self.preview_btn.pack(fill="x", pady=5, padx=10)
        self._components.append(self.preview_btn)
            
        # 行事曆按鈕
        self.calendar_button = tk.Button(
            self.bottom_frame,
            text="行事曆",
            command=self.on_calander_btn_clicked
        )
        self.calendar_button.pack(pady=10, padx=10, fill="x")
        self._components.append(self.calendar_button)

        self.my_items_label = tk.Label(self.bottom_frame, text="─ 我的項目 ─")
        self.my_items_label.pack(pady=10)
        self._components.append(self.my_items_label)

        for project in ["工作", "個人"]:
            btn = tk.Button(self.bottom_frame, text=project)
            btn.pack(fill="x", pady=2, padx=20)
            self._components.append(btn)

        self.tag_add_btn = tk.Button(self.bottom_frame, text="新增標籤", bg="#0077ff", fg="#ffffff", activebackground="#0033ff", activeforeground="#ffffff", 
                                     command=self.on_tag_add_btn_clicked)
        self.tag_add_btn.pack(fill="x", pady=2, padx=20)
        self._components.append(self.tag_add_btn)

        # 設定按鈕
        self.settings_button = tk.Button(
            self.bottom_frame,
            text="設定",
            command=self.on_settings_btn_clicked
        )
        self.settings_button.pack(side="bottom", pady=10, padx=10, fill="x")
        self._components.append(self.settings_button)

        self.add_handler(EventType.FS_CHANGED, self.on_fs_changed)


    def on_index_btn_clicked(self):
        event = Event(EventType.INDEX_BTN_CLICKED, EventData())
        event.emit()

    def on_today_btn_clicked(self):
        event = Event(EventType.TODAY_BTN_CLICKED, EventData())
        event.emit()

    def on_preview_btn_clicked(self):
        event = Event(EventType.PREVIEW_BTN_CLICKED, EventData())
        event.emit()

    def on_calander_btn_clicked(self):
        event = Event(EventType.CALANDER_BTN_CLICKED, EventData())
        event.emit()

    def on_settings_btn_clicked(self):
        event = Event(EventType.SETTINGS_BTN_CLICKED, EventData())
        event.emit()

    def on_tag_add_btn_clicked(self):
        event = Event(EventType.TAG_ADD_BTN_CLICKED, EventData())
        event.emit()

    def on_fs_changed(self, data: FontSizeChangedData):
        for comp in self._components:
            comp.configure(font=font.Font(size=data.font_size))

    def toggle(self):
        if self._frame_open:
            self.frame.configure(width=60)
            self.bottom_frame.pack_forget()
            self.toggle_button.configure(image=self.open_icon)
            self._frame_open = False
        else:
            self.bottom_frame.pack(fill="both", expand=True)
            self.frame.configure(width=200)
            self.toggle_button.configure(image=self.close_icon)
            self._frame_open = True
