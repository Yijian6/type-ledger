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

        # Soft outer shadow
        draw.rounded_rectangle((9, 10, 56, 57), radius=18, fill=(204, 212, 223, 110))

        # Glassy card
        draw.rounded_rectangle((7, 7, 57, 57), radius=18, fill=(255, 255, 255, 248))
        draw.rounded_rectangle((7, 7, 57, 57), radius=18, outline=(228, 232, 238, 255), width=1)
        draw.rounded_rectangle((11, 10, 53, 28), radius=10, fill=(247, 249, 252, 255))

        # Rounded W monogram
        stroke = (86, 90, 98, 255)
        draw.line((18, 21, 24, 43), fill=stroke, width=5, joint="curve")
        draw.line((24, 43, 31, 30), fill=stroke, width=5, joint="curve")
        draw.line((31, 30, 39, 43), fill=stroke, width=5, joint="curve")
        draw.line((39, 43, 46, 21), fill=stroke, width=5, joint="curve")

        # Small soft accent to keep it from feeling sterile
        draw.ellipse((43, 14, 49, 20), fill=(221, 236, 230, 255))

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return Image.open(buffer).copy()
