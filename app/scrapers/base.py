import logging
from abc import ABC, abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup

from app.ml.classifier import classify_domain, classify_difficulty, extract_tags, detect_platform

logger = logging.getLogger(__name__)


class ScrapedProblem:
    def __init__(self, title: str, description: str, domain: Optional[str] = None,
                 organization: Optional[str] = None, category: Optional[str] = None,
                 source_platform: Optional[str] = None, source_year: Optional[int] = None,
                 source_link: Optional[str] = None, tags: Optional[list[str]] = None,
                 difficulty: Optional[str] = None, is_open: bool = True):
        self.title = title
        self.description = description
        self.source_link = source_link or ""
        self.source_platform = source_platform or detect_platform(self.source_link, title, description)
        self.domain = domain or classify_domain(title, description)
        self.organization = organization
        self.category = category
        self.source_year = source_year
        self.tags = tags or extract_tags(title, description)
        self.difficulty = difficulty or classify_difficulty(title, description)
        self.is_open = is_open

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "domain": self.domain,
            "organization": self.organization,
            "category": self.category,
            "source_platform": self.source_platform,
            "source_year": self.source_year,
            "source_link": self.source_link,
            "tags": self.tags,
            "difficulty": self.difficulty,
            "is_open": self.is_open,
        }


class BaseScraper(ABC):
    platform_name = "general"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    @abstractmethod
    def scrape(self) -> list[ScrapedProblem]:
        pass

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def fetch_json(self, url: str) -> Optional[dict]:
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict):
                return data
            logger.warning(f"JSON response from {url} is not a dict (type={type(data).__name__})")
            return None
        except Exception as e:
            logger.error(f"Failed to fetch JSON from {url}: {e}")
            return None
