import calendar
from datetime import date, datetime
from tkinter import messagebox
import tkinter as tk


class CalendarFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.current_year = date.today().year
        self.current_month = date.today().month
        self.selected_date = date.today()
        self.events = {}  # e.g. {'2025-05-10': ['開會']}

        # Header：年份、月份選擇
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)

        self.year_var = tk.StringVar(value=str(self.current_year))
        self.month_var = tk.StringVar(value=str(self.current_month))

        # 年份選擇
        self.year_menu = tk.OptionMenu(nav_frame, values=[str(i) for i in range(2020, 2031)],
                                           variable=self.year_var, command=self.update_calendar)
        self.year_menu.pack(side="left", padx=5)

        # 月份選擇
        self.month_menu = tk.OptionMenu(nav_frame, values=[f"{i}月" for i in range(1, 13)],
                                            variable=self.month_var, command=self.update_calendar)
        self.month_menu.pack(side="left", padx=5)

        # 日曆框
        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack()

        # 行程欄
        self.event_box = tk.Textbox(self, height=100)
        self.event_box.pack(pady=10, fill="x", padx=10)

        # 按鈕
        btn_row = tk.Frame(self)
        btn_row.pack(pady=5)
        tk.Button(btn_row, text="新增行程", command=self.add_event).pack(side="left", padx=10)
        tk.Button(btn_row, text="刪除所有", command=self.delete_event).pack(side="left", padx=10)

        self.draw_calendar()

    def update_calendar(self, *args):
        # 更新年份與月份後繪製日曆
        self.current_year = int(self.year_var.get())
        self.current_month = int(self.month_var.get().replace('月', ''))
        self.draw_calendar()

    def draw_calendar(self):
        # 清空舊的日曆畫面
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(self.current_year, self.current_month)

        # 星期標題列
        header_row = tk.Frame(self.calendar_frame)
        header_row.pack()
        for day in ["一", "二", "三", "四", "五", "六", "日"]:
            lbl = tk.Label(header_row, text=day, width=4)
            lbl.pack(side="left", padx=4)

        # 日期按鈕列
        for week in cal:
            row = tk.Frame(self.calendar_frame)
            row.pack()
            for day in week:
                if day == 0:
                    tk.Label(row, text=" ", width=4).pack(side="left", padx=4)
                else:
                    btn = tk.Button(
                        row,
                        text=str(day),
                        width=4,
                        command=lambda d=day: self.select_day(d)
                    )
                    btn.pack(side="left", padx=4)

    def select_day(self, day):
        # 選擇日期後更新行程框
        self.selected_date = date(self.current_year, self.current_month, day)
        self.update_event_box()

    def update_event_box(self):
        # 更新行程框顯示
        self.event_box.delete("1.0", "end")
        key = self.selected_date.isoformat()
        events = self.events.get(key, [])
        for event in events:
            self.event_box.insert("end", f"{event}\n")

    def add_event(self):
        # 新增行程
        text = self.event_box.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("錯誤", "請輸入行程內容")
            return
        key = self.selected_date.isoformat()
        self.events.setdefault(key, []).append(text)
        messagebox.showinfo("成功", f"已新增行程：{text}")
        self.update_event_box()

    def delete_event(self):
        # 刪除選中日期所有行程
        key = self.selected_date.isoformat()
        if key in self.events:
            del self.events[key]
            messagebox.showinfo("刪除", f"已刪除 {key} 所有行程")
            self.update_event_box()