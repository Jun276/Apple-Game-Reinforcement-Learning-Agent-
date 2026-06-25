"""
Browser controller.
"""

from __future__ import annotations

from playwright.sync_api import Browser
from playwright.sync_api import BrowserContext
from playwright.sync_api import Page
from playwright.sync_api import Playwright
from playwright.sync_api import sync_playwright

from crawler.config import (
    GAME_URL,
    HEADLESS,
    PAGE_LOAD_TIMEOUT,
    VIEWPORT_HEIGHT,
    VIEWPORT_WIDTH,
)
from crawler.logger import get_logger


class BrowserController:

    def __init__(self):

        self.logger = get_logger(self.__class__.__name__)

        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def launch(self) -> Page:

        self.logger.info("Launching browser...")

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS,
        )

        self.context = self.browser.new_context(
            viewport={
                "width": VIEWPORT_WIDTH,
                "height": VIEWPORT_HEIGHT,
            }
        )

        self.page = self.context.new_page()

        self.page.goto(
            GAME_URL,
            timeout=PAGE_LOAD_TIMEOUT,
        )

        self.logger.info("Page loaded.")

        return self.page

    def close(self):

        self.logger.info("Closing browser.")

        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()