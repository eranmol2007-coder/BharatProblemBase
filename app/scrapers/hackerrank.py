import logging

from app.scrapers.base import BaseScraper, ScrapedProblem

logger = logging.getLogger(__name__)


class HackerRankScraper(BaseScraper):
    platform_name = "HackerRank"

    def scrape(self) -> list[ScrapedProblem]:
        logger.info("HackerRank: Scraping not yet implemented (curated data available)")
        return []
