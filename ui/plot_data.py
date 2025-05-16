import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Microsoft JhengHei'

class PlotDataWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("活動圖表")
        self.geometry("800x600")
        self._init_ui()

    def _init_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.activities = self._generate_fake_activities()

        self._init_completion_pie_chart(notebook)
        self._init_weekly_bar_chart(notebook)
        self._init_daily_line_chart(notebook)

    def _init_completion_pie_chart(self, notebook):
        done_count = sum(1 for a in self.activities if a["done"])
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
                if act["starts_at"].date() == day.date():
                    counts[i] += 1

        fig, ax = plt.subplots()
        ax.bar([day.strftime("%a") for day in week], counts, color="skyblue")
        ax.set_title("每週活動數")
        ax.set_ylabel("數量")

        frame = ttk.Frame(notebook)
        self._embed_plot(frame, fig)
        notebook.add(frame, text="每週活動")

    def _init_daily_line_chart(self, notebook):
        today = datetime.today().date()
        hours = list(range(24))
        counts = [0] * 24

        for act in self.activities:
            if act["starts_at"].date() == today:
                hour = act["starts_at"].hour
                counts[hour] += 1

        fig, ax = plt.subplots()
        ax.plot(hours, counts, marker="o", linestyle="-")
        ax.set_title("今日活動分佈")
        ax.set_xlabel("小時")
        ax.set_ylabel("活動數")

        frame = ttk.Frame(notebook)
        self._embed_plot(frame, fig)
        notebook.add(frame, text="每日分佈")

    def _embed_plot(self, container, figure):
        canvas = FigureCanvasTkAgg(figure, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _generate_fake_activities(self):
        now = datetime.now()
        return [
            {
                "starts_at": now - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23)),
                "ends_at": now,
                "done": random.choice([True, False]),
            }
            for _ in range(30)
        ]