import tkinter as tk
from tkinter import ttk
from ui.sidebar import SideBar
from ui.settings_frame import SettingsFrame
from ui.styles_setting import create_light_style, create_dark_style

class SettingsTestApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Testing_Settings_and_Sidebar")
        self.window.minsize(800, 600)

        create_light_style()
        create_dark_style()
        style = ttk.Style(self.window)
        style.theme_use("light")

        self.sidebar = SideBar(self.window, self.on_add_tag_btn_clicked)
        self.sidebar.frame.configure(width=200)
        self.sidebar.frame.pack_propagate(False)
        self.sidebar.frame.pack(side="left", fill="y")

        self.settings_frame = SettingsFrame(self.window)
        self.settings_frame.frame.pack(side="left", fill="both", expand=True)

    def on_add_tag_btn_clicked(self, tag_name: str):
        print(f"模擬按下新增標籤: {tag_name}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = SettingsTestApp()
    app.run()