"""
Template manager.
"""

from __future__ import annotations

from pathlib import Path

from crawler.config import TEMPLATE_DIR


class TemplateManager:

    def __init__(self):

        for number in range(1, 10):

            (
                TEMPLATE_DIR /
                str(number)
            ).mkdir(
                parents=True,
                exist_ok=True,
            )

    def get_directory(
        self,
        number: int,
    ) -> Path:

        return TEMPLATE_DIR / str(number)