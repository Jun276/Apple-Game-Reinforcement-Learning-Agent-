"""
Logging utilities for the crawler.

프로젝트 전역에서 사용하는 Logger를 생성한다.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


_LOGGER_INITIALIZED = False


def _configure_root_logger(log_file: Path | None = None) -> None:
    """
    Configure the root logger.

    Parameters
    ----------
    log_file : Path | None
        Optional log file path.
    """

    global _LOGGER_INITIALIZED

    if _LOGGER_INITIALIZED:
        return

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            filename=log_file,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    _LOGGER_INITIALIZED = True


def get_logger(
    name: str,
    log_file: Path | None = None,
) -> logging.Logger:
    """
    Return configured logger.

    Parameters
    ----------
    name : str
        Logger name.

    log_file : Path |None
        Optional log file path.

    Returns
    -------
    logging.Logger
    """

    _configure_root_logger(log_file)

    return logging.getLogger(name)