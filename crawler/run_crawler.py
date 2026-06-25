"""
Crawler Entry Point
"""

from pathlib import Path

from crawler.board_extractor import BoardExtractor
from crawler.browser_controller import BrowserController
from crawler.canvas_capture import CanvasCapture
from crawler.cell_splitter import CellSplitter
from crawler.config import (
    DEBUG_DIR,
    DIRECTORIES,
)
from crawler.dataset_writer import DatasetWriter
from crawler.logger import get_logger
from crawler.utils import (
    ensure_directories,
    timestamp,
)


logger = get_logger("Crawler")


def main():

    ensure_directories(DIRECTORIES)

    browser = BrowserController()

    try:

        page = browser.launch()

        run_dir = DEBUG_DIR / timestamp()
        run_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        canvas_path = run_dir / "canvas.png"
        board_path = run_dir / "board.png"
        cells_dir = run_dir / "cells"

        CanvasCapture().capture(
            page,
            canvas_path,
        )

        BoardExtractor().extract(
            canvas_path,
            board_path,
        )

        CellSplitter().split(
            board_path,
            cells_dir,
        )

        DatasetWriter().save(
            run_dir / "result.json",
            [],
        )

        input(
            "\nFinished. Press Enter to exit..."
        )

    finally:

        browser.close()


if __name__ == "__main__":

    main()