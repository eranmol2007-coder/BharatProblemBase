import logging

from app.scrapers.base import BaseScraper, ScrapedProblem
from app.ml.classifier import classify_domain, extract_tags, classify_difficulty

logger = logging.getLogger(__name__)


class DevfolioScraper(BaseScraper):
    platform_name = "Devfolio"

    def scrape(self) -> list[ScrapedProblem]:
        problems = []

        problems.extend(self._scrape_website())

        return problems

    def _scrape_website(self) -> list[ScrapedProblem]:
        problems = []
        url = "https://devfolio.co/hackathons"

        soup = self.fetch_page(url)
        if not soup:
            return problems

        cards = soup.select("[class*=hackathon], [class*=card], article, .item")
        if not cards:
            cards = soup.select("a[href*='/hackathon/'], a[href*='hackathons']")

        logger.info(f"Devfolio: Found {len(cards)} potential cards")

        seen = set()
        for card in cards:
            try:
                link_el = card if card.name == "a" and card.get("href") else card.select_one("a[href]")
                if not link_el:
                    continue

                href = link_el.get("href", "")
                if "/hackathon/" not in href and "hackathons" not in href:
                    continue
                if href in seen:
                    continue
                seen.add(href)

                if not href.startswith("http"):
                    href = f"https://devfolio.co{href}"

                title_el = card.select_one("h2, h3, h4, .title, .name, .heading")
                desc_el = card.select_one("p, .description, .desc, .text")

                title = title_el.get_text(strip=True) if title_el else ""
                description = desc_el.get_text(strip=True) if desc_el else ""

                if not title:
                    continue
                if not description:
                    description = f"Hackathon on Devfolio platform. Visit the link for more details."

                problems.append(ScrapedProblem(
                    title=title,
                    description=description,
                    source_platform=self.platform_name,
                    source_link=href,
                    domain=classify_domain(title, description),
                    tags=extract_tags(title, description),
                    difficulty=classify_difficulty(title, description),
                ))

            except Exception as e:
                logger.warning(f"Error parsing Devfolio card: {e}")
                continue

        logger.info(f"Devfolio: Extracted {len(problems)} hackathons")
        return problems
