from __future__ import annotations

import tkinter as tk

from type_record.config import AppConfig
from type_record.storage import DailyCountStore


class CounterWindow:
    def __init__(self, config: AppConfig, store: DailyCountStore) -> None:
        self.config = config
        self.store = store
        self.root = tk.Tk()
        self.root.title(config.app_name)
        self.root.geometry("430x290")
        self.root.minsize(430, 290)
        self.root.configure(bg="#EEF1F4")

        self.count_var = tk.StringVar(value="0")
        self.detail_var = tk.StringVar(value="0 characters today")

        self._build_layout()
        self._schedule_refresh()

    def set_on_close(self, callback) -> None:
        self.root.protocol("WM_DELETE_WINDOW", callback)

    def show(self) -> None:
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide(self) -> None:
        self.root.withdraw()

    def call_in_main_thread(self, callback) -> None:
        self.root.after(0, callback)

    def run(self) -> None:
        self.root.mainloop()

    def destroy(self) -> None:
        self.root.destroy()

    def _build_layout(self) -> None:
        canvas = tk.Canvas(self.root, bg="#EEF1F4", highlightthickness=0, bd=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        canvas.create_oval(-20, -30, 145, 135, fill="#F8FBFF", outline="")
        canvas.create_oval(295, 18, 430, 153, fill="#F7F4FF", outline="")
        canvas.create_oval(320, 205, 470, 355, fill="#F4FAF8", outline="")

        self._rounded_rect(canvas, 33, 38, 401, 250, 34, fill="#E3E8EE", outline="")
        self._rounded_rect(canvas, 28, 30, 397, 245, 34, fill="#FFFFFF", outline="#E5E8ED")

        badge = tk.Frame(canvas, bg="#F6F7F9", padx=10, pady=8)
        tk.Label(
            badge,
            text="W",
            bg="#F6F7F9",
            fg="#545862",
            font=("Segoe UI Semibold", 20),
        ).pack()
        canvas.create_window(342, 76, window=badge, width=58, height=54)

        tk.Label(
            canvas,
            text="TODAY",
            bg="#FFFFFF",
            fg="#8A9099",
            font=("Segoe UI Semibold", 10),
        ).place(x=60, y=66)

        tk.Label(
            canvas,
            text="Writing Count",
            bg="#FFFFFF",
            fg="#16181D",
            font=("SF Pro Display", 20, "bold"),
        ).place(x=60, y=92)

        tk.Label(
            canvas,
            textvariable=self.count_var,
            bg="#FFFFFF",
            fg="#111317",
            font=("SF Pro Display", 54, "bold"),
        ).place(x=56, y=138)

        tk.Label(
            canvas,
            textvariable=self.detail_var,
            bg="#FFFFFF",
            fg="#7A808A",
            font=("Segoe UI", 11),
        ).place(x=61, y=205)

        tk.Label(
            canvas,
            text="Stored locally. No typed content is saved.",
            bg="#FFFFFF",
            fg="#B1B5BC",
            font=("Segoe UI", 9),
        ).place(x=61, y=224)

    def _schedule_refresh(self) -> None:
        count = self.store.get_today_count()
        self.count_var.set(str(count))
        self.detail_var.set(f"{count} characters today")
        self.root.after(self.config.refresh_interval_ms, self._schedule_refresh)

    @staticmethod
    def _rounded_rect(canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, radius: int, **kwargs) -> None:
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)
