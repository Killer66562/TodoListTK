import tkinter as tk


class Task(tk.CTkFrame):
    def __init__(self, master, task_id = None, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.task_id = task_id
        
        self.checkbox = tk.Checkbutton(self)
        self.checkbox.pack(side="left")

        self.label = tk.Label(self, text="AAA")
        self.label.pack(side="right", expand=True, fill="x")