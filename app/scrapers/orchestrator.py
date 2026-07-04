import json
import logging
import os
from typing import Optional

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.problem_statement import ProblemStatement
from app.scrapers.sih import SIHScraper
from app.scrapers.devfolio import DevfolioScraper
from app.scrapers.hackerearth import HackerEarthScraper
from app.scrapers.unstop import UnstopScraper
from app.scrapers.d2c import D2CScraper
from app.scrapers.codechef import CodeChefScraper
from app.scrapers.hackerrank import HackerRankScraper
from app.scrapers.mlh import MLHScraper
from app.scrapers.devpost import DevpostScraper
from app.ml.classifier import classify_domain, extract_tags, classify_difficulty

logger = logging.getLogger(__name__)


class ScraperOrchestrator:
    def __init__(self):
        self.scrapers = [
            SIHScraper(),
            DevfolioScraper(),
            HackerEarthScraper(),
            UnstopScraper(),
            D2CScraper(),
            CodeChefScraper(),
            HackerRankScraper(),
            MLHScraper(),
            DevpostScraper(),
        ]

    def scrape_all(self, db: Optional[Session] = None) -> dict:
        results = {"total": 0, "new": 0, "platforms": {}}
        close_db = False
        if db is None:
            db = SessionLocal()
            close_db = True

        try:
            for scraper in self.scrapers:
                try:
                    scraped = scraper.scrape()
                    platform = scraper.platform_name
                    count = len(scraped)
                    new_count = self._store_problems(db, scraped)

                    results["platforms"][platform] = {
                        "found": count,
                        "new": new_count,
                    }
                    results["total"] += count
                    results["new"] += new_count

                    logger.info(f"{platform}: found {count}, new {new_count}")

                except Exception as e:
                    logger.error(f"Error scraping {scraper.platform_name}: {e}")
                    results["platforms"][scraper.platform_name] = {
                        "error": str(e)
                    }
                    continue

            curated_count = self._load_curated(db)
            if curated_count > 0:
                results["curated"] = curated_count
                results["new"] += curated_count
                results["total"] += curated_count

            return results

        finally:
            if close_db:
                db.close()

    def _store_problems(self, db: Session, problems: list) -> int:
        new_count = 0
        for problem in problems:
            exists = db.query(ProblemStatement).filter(
                ProblemStatement.title == problem.title
            ).first()
            if not exists:
                db.add(ProblemStatement(**problem.to_dict()))
                new_count += 1
        if new_count > 0:
            db.commit()
        return new_count

    def _load_curated(self, db: Session) -> int:
        curated_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data", "curated_problems.json"
        )
        if not os.path.isfile(curated_path):
            return 0

        try:
            with open(curated_path, "r", encoding="utf-8") as f:
                items = json.load(f)

            existing_titles = set(
                row[0] for row in db.query(ProblemStatement.title).all()
            )

            new_problems = []
            for item in items:
                if item["title"] in existing_titles:
                    continue
                if not item.get("domain"):
                    item["domain"] = classify_domain(item["title"], item["description"])
                if not item.get("tags"):
                    item["tags"] = extract_tags(item["title"], item["description"])
                if not item.get("difficulty"):
                    item["difficulty"] = classify_difficulty(item["title"], item["description"])
                new_problems.append(ProblemStatement(**item))

            if new_problems:
                db.add_all(new_problems)
                db.commit()
                logger.info(f"Loaded {len(new_problems)} curated problems")

            return len(new_problems)

        except Exception as e:
            logger.error(f"Error loading curated data: {e}")
            return 0
