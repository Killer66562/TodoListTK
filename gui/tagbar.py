import tkinter as tk

from enums.enums import EventType
from events.data import ActivitiesLoadData, TagRemoveData, TagSelectedData
from events.events import Event


class TagBar:
    def __init__(self, master, tag_name: str):
        self.tag_name = tag_name

        self.frame = tk.Frame(master)

        self.btn = tk.Button(self.frame, text=tag_name)
        self.btn.pack(side="left", fill="x", expand=True)

        self.delete_btn = tk.Button(self.frame, text="x", bg="red", activebackground="red", command=self.on_delete_btn_clicked)
        self.delete_btn.pack(side="right")
    
    def on_btn_clicked(self):
        event = Event(EventType.ACTIVITIES_LOAD, ActivitiesLoadData(self.tag_name))
        event.emit()
        
    def on_delete_btn_clicked(self):
        event = Event(EventType.TAG_REMOVE, TagRemoveData(name=self.tag_name))