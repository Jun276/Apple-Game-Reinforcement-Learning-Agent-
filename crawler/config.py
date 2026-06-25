"""
Crawler Configuration

프로젝트 전역에서 사용하는 설정값을 관리한다.
"""

from pathlib import Path

# ==========================================================
# Project
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_ROOT / "datasets"
DEBUG_DIR = DATASET_DIR / "debug"
BOARD_DIR = DATASET_DIR / "boards"
TEMPLATE_DIR = DATASET_DIR / "templates"

# ==========================================================
# Game
# ==========================================================

GAME_URL = (
    "https://apple.oshizi.com/ko/play/"
    "Mmokm3V5miNtkpbi1IZq0IGyWC9GNX4F4hm_CRFF4hpipkAEF_"
    "O8QyWOcCZ_US-csOY5U4E3aoHY3AiCtKKjs5iuDE3II-/"
)

BOARD_ROWS = 10
BOARD_COLS = 17
CELL_COUNT = BOARD_ROWS * BOARD_COLS

# ==========================================================
# Browser
# ==========================================================

HEADLESS = False

VIEWPORT_WIDTH = 1600
VIEWPORT_HEIGHT = 1000

PAGE_LOAD_TIMEOUT = 30_000

# ==========================================================
# Capture
# ==========================================================

CAPTURE_RETRY = 5
CAPTURE_INTERVAL = 0.3

# ==========================================================
# Debug
# ==========================================================

DEBUG = True

SAVE_DEBUG_IMAGE = True
SAVE_CELL_IMAGES = True

# ==========================================================
# Recognition
# ==========================================================

TEMPLATE_MATCH_THRESHOLD = 0.90

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = "INFO"

# ==========================================================
# Directory Initialization
# ==========================================================

DIRECTORIES = (
    DATASET_DIR,
    DEBUG_DIR,
    BOARD_DIR,
    TEMPLATE_DIR,
)