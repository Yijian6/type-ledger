from __future__ import annotations

from io import BytesIO
from threading import Thread
from typing import Callable

import pystray
from PIL import Image, ImageDraw


class TrayController:
    def __init__(
        self,
        tooltip: str,
        on_show: Callable[[], None],
        on_exit: Callable[[], None],
    ) -> None:
        self.tooltip = tooltip
        self.on_show = on_show
        self.on_exit = on_exit
        self._icon: pystray.Icon | None = None
        self._thread: Thread | None = None

    def start(self) -> None:
        if self._thread is not None:
            return

        menu = pystray.Menu(
            pystray.MenuItem("Show Window", self._handle_show, default=True),
            pystray.MenuItem("Exit", self._handle_exit),
        )
        self._icon = pystray.Icon(
            "type_record",
            self._build_icon_image(),
            self.tooltip,
            menu,
        )
        self._thread = Thread(target=self._icon.run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._icon is not None:
            self._icon.stop()
        self._icon = None
        self._thread = None

    def _handle_show(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        _ = (icon, item)
        self.on_show()

    def _handle_exit(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        _ = (icon, item)
        self.on_exit()

    def _build_icon_image(self) -> Image.Image:
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle((8, 9, 56, 57), radius=19, fill=(228, 233, 239, 150))
        draw.rounded_rectangle((6, 6, 58, 58), radius=20, fill=(255, 255, 255, 248))
        draw.rounded_rectangle((7, 7, 57, 57), radius=19, outline=(229, 232, 237, 255), width=1)

        accent = (244, 246, 249, 255)
        draw.ellipse((12, 10, 35, 28), fill=accent)

        stroke = (80, 85, 94, 255)
        draw.line((18, 20, 24, 44), fill=stroke, width=6)
        draw.line((24, 44, 31, 29), fill=stroke, width=6)
        draw.line((31, 29, 39, 44), fill=stroke, width=6)
        draw.line((39, 44, 46, 20), fill=stroke, width=6)

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return Image.open(buffer).copy()
