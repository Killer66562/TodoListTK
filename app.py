from gui.calendar import CalendarFrame
import tkinter as tk
from events.data import EventData, InputRowBtnClickedData
from events.listener import EventListener
from enums.enums import FrameType, EventType
from gui.add_tag import AddTag
from gui.input_row import InputRow
from gui.sidebar import Sidebar
from gui.settings import Settings


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
        self.settings = Settings(self.window)
        self.calendar = CalendarFrame(self.window)

        self.current_frame = None

        self.add_handler(EventType.INPUT_ROW_BTN_CLICKED, self.input_data_handler)
        self.add_handler(EventType.TAG_ADD_BTN_CLICKED, self.on_add_tag_btn_clicked_event)
        self.add_handler(EventType.CALANDER_BTN_CLICKED, self.on_calendar_btn_clicked)
        self.add_handler(EventType.SETTINGS_BTN_CLICKED, self.on_settings_btn_clicked)

    def switch_frame(self, frame: tk.Frame):
        if self.current_frame is frame:
            return
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.update()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def on_settings_btn_clicked(self, data: EventData):
        self.switch_frame(self.settings.frame)

    def on_add_tag_btn_clicked_event(self, data: EventData):
        if not self.add_tag:
            self.add_tag = AddTag(self.window)
            self.add_tag.window.bind("<Destroy>", self.on_add_tag_destroy)
            self.add_tag.window.focus()
            self.add_tag.window.mainloop()

    def on_calendar_btn_clicked(self, data: EventData):
        self.switch_frame(self.calendar.frame)

    def on_add_tag_destroy(self, _):
        self.add_tag = None

    def input_data_handler(self, data: InputRowBtnClickedData):
        print(data.frame_type)
        print(data.value)

    def run(self):
        self.switch_frame(self.input_row.frame)
        self.window.mainloop()


app = TodoList()
app.run()