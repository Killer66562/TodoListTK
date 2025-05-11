import tkinter as tk
from tkinter import font
from events.listener import EventListener
from gui.popup import Popup
from events.events import Event
from events.data import EventData, FontSizeChangedData, InputRowBtnClickedData
from enums.enums import EventType, FrameType


class InputRow(EventListener):
    def __init__(self, master, frame_type: FrameType, name: str = ""):
        super().__init__()
        self.frame_type = frame_type

        self.text_var = tk.StringVar(value="")

        self.frame = tk.Frame(master)

        self.label = tk.Label(self.frame, text=name)
        self.label.pack(side="top", anchor="w")

        self.bottom_frame = tk.Frame(self.frame)
        self.bottom_frame.pack(fill="x")

        self.entry = tk.Entry(self.bottom_frame, textvariable=self.text_var)
        self.entry.pack(side="left", expand=True, fill="x")

        self.btn = tk.Button(self.bottom_frame, command=self.on_btn_clicked, text="Add")
        self.btn.pack(side="right")

        self.add_handler(EventType.INDEX_BTN_CLICKED, self.on_index_event)
        self.add_handler(EventType.TODAY_BTN_CLICKED, self.on_today_event)
        self.add_handler(EventType.PREVIEW_BTN_CLICKED, self.on_preview_event)
        self.add_handler(EventType.FS_CHANGED, self.on_fs_changed)

    def on_fs_changed(self, data: FontSizeChangedData):
        self.label.configure(font=font.Font(size=data.font_size))
        self.btn.configure(font=font.Font(size=data.font_size))
        self.entry.configure(font=font.Font(size=data.font_size))

    def on_index_event(self, data: EventData):

        self.label.configure(text="收件箱")

    def on_today_event(self, data: EventData):
        self.label.configure(text="今天")

    def on_preview_event(self, data: EventData):
        self.label.configure(text="預覽")

    def on_btn_clicked(self):
        event = Event(
            EventType.INPUT_ROW_BTN_CLICKED, 
            InputRowBtnClickedData(self.frame_type, self.text_var.get())
        )
        event.emit()
        self.text_var.set("")
