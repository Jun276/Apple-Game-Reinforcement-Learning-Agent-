"""
Canvas capture module.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from playwright.sync_api import Page

from crawler.logger import get_logger


class CanvasCapture:

    def __init__(self):

        self.logger = get_logger(self.__class__.__name__)

    def capture(
        self,
        page: Page,
        output_path: Path,
    ) -> Path:

        canvas = page.locator("canvas").first

        canvas.screenshot(path=str(output_path))

        self.logger.info(
            "Canvas saved -> %s",
            output_path,
        )

        return output_path

    def load(
        self,
        image_path: Path,
    ) -> Image.Image:

        return Image.open(image_path)