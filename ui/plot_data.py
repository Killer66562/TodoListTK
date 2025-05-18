import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from models import local

plt.rcParams['font.family'] = 'Microsoft JhengHei'


class PlotDataWindow(tk.Toplevel):
    def __init__(self, master=None, activities: list[local.Activity] | list = None):
        super().__init__(master)
        self.title("活動圖表")
        self.geometry("800x600")

        self.activities = activities

        self._init_ui()

    def _init_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self._init_completion_pie_chart(notebook)
        self._init_weekly_bar_chart(notebook)

    def _init_completion_pie_chart(self, notebook):
        done_count = sum(1 for a in self.activities if a.done)
        undone_count = len(self.activities) - done_count

        fig, ax = plt.subplots()
        ax.pie([done_count, undone_count], labels=["完成", "未完成"], autopct="%1.1f%%", colors=["green", "red"])
        ax.set_title("活動完成比例")

        frame = ttk.Frame(notebook)
        self._embed_plot(frame, fig)
        notebook.add(frame, text="完成比例")

    def _init_weekly_bar_chart(self, notebook):
        today = datetime.today()
        week = [today - timedelta(days=i) for i in range(6, -1, -1)]
        counts = [0] * 7

        for act in self.activities:
            for i, day in enumerate(week):
                if act.starts_at.date() == day.date():
                    counts[i] += 1

        fig, ax = plt.subplots()
        ax.bar([day.strftime("%a") for day in week], counts, color="skyblue")
        ax.set_title("每週活動數")
        ax.set_ylabel("數量")
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        frame = ttk.Frame(notebook)
        self._embed_plot(frame, fig)
        notebook.add(frame, text="每週活動")

    def _embed_plot(self, container, figure):
        canvas = FigureCanvasTkAgg(figure, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)