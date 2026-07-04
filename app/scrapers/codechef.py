import logging

from app.scrapers.base import BaseScraper, ScrapedProblem

logger = logging.getLogger(__name__)


class CodeChefScraper(BaseScraper):
    platform_name = "CodeChef"

    def scrape(self) -> list[ScrapedProblem]:
        logger.info("CodeChef: Scraping not yet implemented (curated data available)")
        return []
