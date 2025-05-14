import tkinter as tk
from tkinter import ttk
from ui.sidebar import SideBar
from ui.plot_data import PlotDataFrame
from ui.styles_setting import create_light_style, create_dark_style


class PlotDataTestApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Testing_PlotData_and_Sidebar")
        self.window.minsize(1000, 700)

        create_light_style()
        create_dark_style()
        style = ttk.Style(self.window)
        style.theme_use("light")

        self.sidebar = SideBar(self.window, self.on_dummy_callback)
        self.sidebar.frame.configure(width=200)
        self.sidebar.frame.pack_propagate(False)
        self.sidebar.frame.pack(side="left", fill="y")

        self.plot_data_frame = PlotDataFrame(self.window)
        self.plot_data_frame.frame.pack(side="left", fill="both", expand=True)

    def on_dummy_callback(self, *args, **kwargs):
        print("模擬 Sidebar 中某個按鈕被點擊")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = PlotDataTestApp()
    app.run()