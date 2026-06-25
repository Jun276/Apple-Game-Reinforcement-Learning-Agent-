"""
Board extraction module.

현재 버전에서는 Canvas 전체를 보드 이미지로 사용한다.
향후 자동 보드 검출 알고리즘으로 교체할 예정이다.
"""

from __future__ import annotations

from pathlib import Path

import cv2

from crawler.logger import get_logger


class BoardExtractor:

    def __init__(self):

        self.logger = get_logger(self.__class__.__name__)

    def extract(
        self,
        canvas_path: Path,
        output_path: Path,
    ) -> Path:

        image = cv2.imread(str(canvas_path))

        if image is None:
            raise FileNotFoundError(canvas_path)

        cv2.imwrite(
            str(output_path),
            image,
        )

        self.logger.info(
            "Board extracted -> %s",
            output_path,
        )

        return output_path