import logging
import re

from app.scrapers.base import BaseScraper, ScrapedProblem
from app.ml.classifier import classify_domain, extract_tags

logger = logging.getLogger(__name__)


class HackerEarthScraper(BaseScraper):
    platform_name = "HackerEarth"

    def scrape(self) -> list[ScrapedProblem]:
        problems = []
        seen_titles = set()

        urls = [
            "https://www.hackerearth.com/challenges/hackathon/",
            "https://www.hackerearth.com/challenges/hackathon/?page=1&status=all",
        ]
        for url in urls:
            soup = self.fetch_page(url)
            if not soup:
                continue

            cards = soup.select(".challenge-card-modern")
            for card in cards:
                try:
                    title = self._extract_title(card)
                    if not title or title in seen_titles:
                        continue
                    seen_titles.add(title)

                    link_el = card.select_one("a[href*='/hackathon/']")
                    href = link_el.get("href", "") if link_el else ""
                    if href and not href.startswith("http"):
                        href = f"https://www.hackerearth.com{href}"

                    org_el = card.select_one(".company-details, .company-detail, .company-name, .dark")
                    organization = org_el.get_text(strip=True) if org_el else "HackerEarth"
                    if organization == title[:len(organization)]:
                        organization = "HackerEarth"

                    full_text = card.get_text(" ", strip=True)
                    deadline = self._extract_deadline(full_text)

                    description = self._build_description(title, organization, deadline)
                    source_year = self._extract_year(deadline)
                    is_open = "ENDS IN" in full_text.upper() or not deadline

                    problems.append(ScrapedProblem(
                        title=title,
                        description=description,
                        source_platform=self.platform_name,
                        source_link=href or url,
                        source_year=source_year,
                        organization=organization,
                        domain=classify_domain(title, description),
                        tags=extract_tags(title, description),
                        is_open=is_open,
                    ))
                except Exception as e:
                    continue

        logger.info(f"HackerEarth: Extracted {len(problems)} challenges (page shows only JS-rendered content)")
        return problems

    def _extract_title(self, card) -> str:
        for sel in [".challenge-list-title", ".title", ".name", "h2", "h3", "h4", "[class*=title]"]:
            el = card.select_one(sel)
            if el:
                t = el.get_text(strip=True)
                if t:
                    return t
        return ""

    def _extract_deadline(self, text: str) -> str:
        for pattern in [
            r'ENDS IN\s*:\s*:?\s*([^R]+)',
            r'STARTS ON\s*([^R]+)',
            r'([A-Z][a-z]+ \d{1,2}, \d{4})',
        ]:
            m = re.search(pattern, text)
            if m:
                return m.group(1).strip()
        return ""

    def _extract_year(self, deadline: str) -> int:
        m = re.search(r'(\d{4})', deadline)
        return int(m.group(1)) if m else 2026

    def _build_description(self, title: str, org: str, deadline: str) -> str:
        parts = [f"Hackathon challenge organized by {org}."]
        if deadline:
            parts.append(f"Timeline: {deadline}.")
        parts.append(f"Participants are invited to build and submit their solutions for '{title}'.")
        return " ".join(parts)
