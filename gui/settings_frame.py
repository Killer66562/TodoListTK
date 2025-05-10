import tkinter as tk


class SettingsFrame(tk.Frame):
    def __init__(self, master, root, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.root = root

        self.font_var = tk.IntVar(value=12)
        self.color_var = tk.StringVar(value="green")

        self.title = tk.Label(self, font=tk.Font('Arial', size=28), text="Settings")
        self.title.pack()

        self.font_size_label = tk.Label(self, text="字體大小")
        self.font_size_label.pack(ipadx=5, ipady=5)

        self.font_size_scrollbar = tk.Scale(self, from_=12, to=24, number_of_steps=16, command=self.on_fs_changed, variable=self.font_var)
        self.font_size_scrollbar.pack(ipadx=5, ipady=5, fill="x")

        self.font_size_show_label = tk.Label(self, text="12")
        self.font_size_show_label.pack()

    def on_fs_changed(self, _):
        fs = self.font_var.get()
        self.font_size_show_label.configure(text=str(fs))



