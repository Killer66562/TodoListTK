import tkinter as tk
from events.data import EventData, InputRowBtnClickedData
from events.listener import EventListener
from enums.enums import FrameType, EventType
from gui.add_tag import AddTag
from gui.input_row import InputRow
from gui.sidebar import Sidebar


class TodoList(EventListener):
    def __init__(self):
        super().__init__()
        self.add_tag = None

        self.window = tk.Tk()
        self.window.title("TodoList")
        self.window.minsize(800, 600)

        self.sidebar = Sidebar(self.window)
        self.sidebar.frame.pack(side="left", fill="y")

        self.input_row = InputRow(self.window, FrameType.INDEX, "Test")
        self.input_row.frame.pack(fill="x")

        self.add_handler(EventType.INPUT_ROW_BTN_CLICKED, self.input_data_handler)
        self.add_handler(EventType.TAG_ADD_BTN_CLICKED, self.on_add_tag_btn_clicked_event)

    def on_add_tag_btn_clicked_event(self, data: EventData):
        if not self.add_tag:
            self.add_tag = AddTag(self.window)
            self.add_tag.window.bind("<Destroy>", self.on_add_tag_destroy)
            self.add_tag.window.focus()
            self.add_tag.window.mainloop()

    def on_add_tag_destroy(self, _):
        self.add_tag = None

    def input_data_handler(self, data: InputRowBtnClickedData):
        print(data.frame_type)
        print(data.value)

    def run(self):
        self.window.mainloop()


app = TodoList()
app.run()