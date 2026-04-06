from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    app_name: str = "Type Record"
    count_space: bool = True
    count_enter: bool = False
    backspace_decrements: bool = True
    refresh_interval_ms: int = 300
    tray_tooltip: str = "Type Record"
    start_hidden_to_tray: bool = True

    @property
    def data_file(self) -> Path:
        # Prefer APPDATA on Windows. storage.py will fall back to a local data
        # directory if that path is not writable on this machine.
        appdata = os.environ.get("APPDATA")
        base_dir = Path(appdata) if appdata else Path.cwd()
        return base_dir / "TypeRecord" / "data" / "daily_counts.json"
