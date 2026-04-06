from __future__ import annotations

from dataclasses import dataclass

import keyboard

from type_record.config import AppConfig
from type_record.storage import DailyCountStore


IGNORED_KEYS = {
    "shift",
    "left shift",
    "right shift",
    "ctrl",
    "left ctrl",
    "right ctrl",
    "alt",
    "left alt",
    "right alt",
    "alt gr",
    "windows",
    "left windows",
    "right windows",
    "caps lock",
    "tab",
    "esc",
    "up",
    "down",
    "left",
    "right",
    "insert",
    "delete",
    "home",
    "end",
    "page up",
    "page down",
    "print screen",
    "menu",
}


@dataclass
class KeyboardCounter:
    config: AppConfig
    store: DailyCountStore

    def __post_init__(self) -> None:
        self._hook = None

    def start(self) -> None:
        if self._hook is not None:
            return
        self._hook = keyboard.on_press(self._handle_key_event, suppress=False)

    def stop(self) -> None:
        if self._hook is None:
            return
        keyboard.unhook(self._hook)
        self._hook = None

    def _handle_key_event(self, event: keyboard.KeyboardEvent) -> None:
        key_name = (event.name or "").lower()
        if not key_name or key_name in IGNORED_KEYS:
            return

        delta = self._resolve_delta(key_name)
        if delta != 0:
            self.store.increment(delta)

    def _resolve_delta(self, key_name: str) -> int:
        if len(key_name) == 1:
            return 1

        if key_name == "space":
            return 1 if self.config.count_space else 0

        if key_name == "enter":
            return 1 if self.config.count_enter else 0

        if key_name == "backspace":
            # MVP 的简单策略：
            # 把 Backspace 当成“撤销最近 1 个字符”，这样更接近最终保留下来的文本量。
            # 这个方案不会追踪真实文本内容，因此对批量删除、删除历史文本等场景并不精确。
            return -1 if self.config.backspace_decrements else 0

        return 0
