"""
Debug image utilities.
"""

from __future__ import annotations

from pathlib import Path

import cv2


class DebugView:

    def save_overlay(
        self,
        image_path: Path,
        output_path: Path,
    ) -> None:

        image = cv2.imread(str(image_path))

        cv2.imwrite(
            str(output_path),
            image,
        )