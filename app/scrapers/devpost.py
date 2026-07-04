import logging
from app.scrapers.base import BaseScraper, ScrapedProblem
logger = logging.getLogger(__name__)

class DevpostScraper(BaseScraper):
    platform_name = "Devpost"
    def scrape(self) -> list[ScrapedProblem]:
        logger.info("Devpost: Scraping not yet implemented (curated data available)")
        return []
