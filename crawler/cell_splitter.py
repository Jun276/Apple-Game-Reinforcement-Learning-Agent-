"""
Split board image into 17x10 cells.
"""

from __future__ import annotations

from pathlib import Path

import cv2

from crawler.config import (
    BOARD_COLS,
    BOARD_ROWS,
)
from crawler.logger import get_logger


class CellSplitter:

    def __init__(self):

        self.logger = get_logger(self.__class__.__name__)

    def split(
        self,
        board_path: Path,
        output_dir: Path,
    ) -> list[Path]:

        image = cv2.imread(str(board_path))

        if image is None:
            raise FileNotFoundError(board_path)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        height, width = image.shape[:2]

        cell_width = width // BOARD_COLS
        cell_height = height // BOARD_ROWS

        saved = []

        index = 0

        for row in range(BOARD_ROWS):

            for col in range(BOARD_COLS):

                x1 = col * cell_width
                y1 = row * cell_height

                x2 = x1 + cell_width
                y2 = y1 + cell_height

                cell = image[y1:y2, x1:x2]

                save_path = output_dir / f"{index:03d}.png"

                cv2.imwrite(
                    str(save_path),
                    cell,
                )

                saved.append(save_path)

                index += 1

        self.logger.info(
            "%d cells generated.",
            len(saved),
        )

        return saved