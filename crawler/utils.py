"""
Utility functions for the crawler.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def ensure_directory(path: Path) -> None:
    """
    Create directory if it does not exist.
    """
    path.mkdir(parents=True, exist_ok=True)


def ensure_directories(paths: list[Path] | tuple[Path, ...]) -> None:
    """
    Create multiple directories.
    """
    for path in paths:
        ensure_directory(path)


def timestamp() -> str:
    """
    Return current timestamp.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_json(path: Path, data: dict[str, Any]) -> None:
    """
    Save JSON file.
    """
    ensure_directory(path.parent)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4,
        )


def load_json(path: Path) -> dict[str, Any]:
    """
    Load JSON file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)