"""
Template based digit classifier.

현재는 Placeholder.

다음 버전에서 Template Matching 구현.
"""

from __future__ import annotations

from pathlib import Path


class DigitClassifier:

    def predict(
        self,
        cell_path: Path,
    ) -> int:

        # TODO
        return 0

    def predict_batch(
        self,
        cell_paths: list[Path],
    ) -> list[int]:

        return [
            self.predict(cell)
            for cell in cell_paths
        ]