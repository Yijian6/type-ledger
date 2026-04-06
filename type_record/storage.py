from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from threading import Lock


@dataclass
class DailyCountStore:
    file_path: Path

    def __post_init__(self) -> None:
        self._lock = Lock()
        self.file_path = self._resolve_writable_path(self.file_path)
        self._state = self._load()
        self._ensure_today_record()

    def get_today_count(self) -> int:
        with self._lock:
            self._ensure_today_record()
            return int(self._state["count"])

    def increment(self, delta: int) -> int:
        with self._lock:
            self._ensure_today_record()
            next_value = max(0, int(self._state["count"]) + delta)
            self._state["count"] = next_value
            self._save()
            return next_value

    def _today_str(self) -> str:
        return date.today().isoformat()

    def _resolve_writable_path(self, preferred_path: Path) -> Path:
        try:
            preferred_path.parent.mkdir(parents=True, exist_ok=True)
            return preferred_path
        except OSError:
            fallback_path = Path.cwd() / "data" / "daily_counts.json"
            fallback_path.parent.mkdir(parents=True, exist_ok=True)
            return fallback_path

    def _ensure_today_record(self) -> None:
        today = self._today_str()
        if self._state.get("date") != today:
            self._state = {"date": today, "count": 0}
            self._save()

    def _load(self) -> dict:
        if not self.file_path.exists():
            return {"date": self._today_str(), "count": 0}

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return {"date": self._today_str(), "count": 0}

        if not isinstance(data, dict):
            return {"date": self._today_str(), "count": 0}

        return {
            "date": str(data.get("date", self._today_str())),
            "count": max(0, int(data.get("count", 0))),
        }

    def _save(self) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self._state, file, ensure_ascii=False, indent=2)
