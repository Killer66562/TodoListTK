import tkinter as tk


class NumberEntry(tk.Frame):
    def __init__(self, master, var: tk.DoubleVar, min_val: float = 0.0, max_val: float = 10.0, step: float = 1.0, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self._min_val = min_val
        self._max_val = max_val
        self._step = step
        
        self._var = var

        self.minus_btn = tk.Button(self, width=28, height=28, text="-", command=self.on_minus_btn_clicked)
        self.minus_btn.pack(side="left")

        self.entry = tk.Entry(self, textvariable=var, state="disabled")
        self.entry.pack(side="left")

        self.plus_btn = tk.Button(self, width=28, height=28, text="+", command=self.on_plus_btn_clicked)
        self.plus_btn.pack(side="left")

    def on_minus_btn_clicked(self):
        var_val = self._var.get()
        self._var.set(max(var_val - self._step, self._min_val))

    def on_plus_btn_clicked(self):
        var_val = self._var.get()
        self._var.set(min(var_val + self._step, self._max_val))