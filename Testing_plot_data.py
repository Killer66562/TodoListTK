import tkinter as tk
from tkinter import ttk
from ui.sidebar import SideBar
from ui.plot_data import PlotDataWindow
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

        button = ttk.Button(self.window, text="圖表視窗", command=self.open_plot_window)
        button.pack(pady=20)

    def open_plot_window(self):
        PlotDataWindow(master=self.window)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = PlotDataTestApp()
    app.run()