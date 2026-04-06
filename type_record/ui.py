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
        self.root.geometry("420x270")
        self.root.minsize(420, 270)
        self.root.configure(bg="#EDF1F5")

        self.count_var = tk.StringVar(value="0")
        self.detail_var = tk.StringVar(value="0 today")

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
        shell = tk.Frame(self.root, bg="#EDF1F5", padx=22, pady=22)
        shell.pack(fill=tk.BOTH, expand=True)

        shadow = tk.Frame(shell, bg="#E3E8EE", bd=0)
        shadow.pack(fill=tk.BOTH, expand=True, padx=(4, 0), pady=(4, 0))

        card = tk.Frame(shadow, bg="#FFFFFF", bd=0)
        card.place(x=-4, y=-4, relwidth=1.0, relheight=1.0)

        top = tk.Frame(card, bg="#FFFFFF", padx=28, pady=24)
        top.pack(fill=tk.X)

        left = tk.Frame(top, bg="#FFFFFF")
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            left,
            text="TODAY",
            bg="#FFFFFF",
            fg="#969BA3",
            font=("Segoe UI Semibold", 10),
        ).pack(anchor=tk.W)

        tk.Label(
            left,
            text="Typing Count",
            bg="#FFFFFF",
            fg="#14161A",
            font=("Segoe UI Semibold", 18),
        ).pack(anchor=tk.W, pady=(6, 0))

        token = tk.Frame(top, bg="#F7F8FA", padx=16, pady=10)
        token.pack(side=tk.RIGHT)

        tk.Label(
            token,
            text="W",
            bg="#F7F8FA",
            fg="#575C66",
            font=("Segoe UI Semibold", 18),
        ).pack()

        body = tk.Frame(card, bg="#FFFFFF", padx=28, pady=0)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            body,
            textvariable=self.count_var,
            bg="#FFFFFF",
            fg="#111317",
            font=("Segoe UI", 56, "bold"),
        ).pack(anchor=tk.W, pady=(8, 0))

        tk.Label(
            body,
            textvariable=self.detail_var,
            bg="#FFFFFF",
            fg="#7D838C",
            font=("Segoe UI", 11),
        ).pack(anchor=tk.W, pady=(6, 0))

        footer = tk.Frame(card, bg="#FFFFFF", padx=28, pady=20)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(
            footer,
            text="Local only. No text content stored.",
            bg="#FFFFFF",
            fg="#B1B6BD",
            font=("Segoe UI", 9),
        ).pack(anchor=tk.W)

    def _schedule_refresh(self) -> None:
        count = self.store.get_today_count()
        self.count_var.set(str(count))
        self.detail_var.set(f"{count} today")
        self.root.after(self.config.refresh_interval_ms, self._schedule_refresh)
