import logging
from app.scrapers.base import BaseScraper, ScrapedProblem
logger = logging.getLogger(__name__)

class MLHScraper(BaseScraper):
    platform_name = "MLH"
    def scrape(self) -> list[ScrapedProblem]:
        logger.info("MLH: Scraping not yet implemented (curated data available)")
        return []
