"""
Dataset writer.
"""

from __future__ import annotations

from pathlib import Path

from crawler.utils import save_json


class DatasetWriter:

    def save(
        self,
        output_path: Path,
        board: list[list[int]],
    ) -> None:

        data = {
            "rows": len(board),
            "cols": len(board[0]),
            "board": board,
        }

        save_json(
            output_path,
            data,
        )