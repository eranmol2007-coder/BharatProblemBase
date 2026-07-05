import logging
import time

from app.scrapers.base import BaseScraper, ScrapedProblem
from app.ml.classifier import classify_domain, extract_tags, classify_difficulty

logger = logging.getLogger(__name__)

MAX_PAGES = 50
PER_PAGE = 100


class UnstopScraper(BaseScraper):
    platform_name = "Unstop"

    def scrape(self) -> list[ScrapedProblem]:
        problems = []

        problems.extend(self._scrape_with_cookies())
        problems.extend(self._scrape_via_api())

        return problems

    def _scrape_with_cookies(self) -> list[ScrapedProblem]:
        problems = []
        url = "https://unstop.com/hackathons"

        self.session.cookies.set("cookie_consent", "true", domain="unstop.com")
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })

        soup = self.fetch_page(url)
        if not soup:
            return problems

        if "Cookies Disabled" in soup.get_text():
            logger.warning("Unstop: Cookies required, trying alternative approach")
            return self._scrape_via_api()

        cards = soup.select("[class*=card], [class*=hackathon], [class*=opportunity], [class*=listing]")
        logger.info(f"Unstop: Found {len(cards)} potential cards")

        seen = set()
        for card in cards:
            try:
                title_el = card.select_one("h2, h3, h4, .title, .card-title, .name, .heading")
                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                if not title or title in seen:
                    continue
                seen.add(title)

                desc_el = card.select_one("p, .description, .card-text, .desc")
                description = desc_el.get_text(strip=True) if desc_el else ""

                link_el = card.select_one("a[href]")
                href = link_el.get("href", "") if link_el else ""
                if href and not href.startswith("http"):
                    href = f"https://unstop.com{href}"

                if not description:
                    description = f"Hackathon/competition on Unstop platform."

                problems.append(ScrapedProblem(
                    title=title,
                    description=description,
                    source_platform=self.platform_name,
                    source_link=href or url,
                    domain=classify_domain(title, description),
                    tags=extract_tags(title, description),
                    difficulty=classify_difficulty(title, description),
                ))
            except Exception as e:
                continue

        return problems

    def _scrape_via_api(self) -> list[ScrapedProblem]:
        problems = []
        seen = set()
        api_base_urls = [
            ("https://unstop.com/api/public/opportunity/search?opportunity_type=hackathons", "hackathons"),
            ("https://unstop.com/api/public/opportunity/search?opportunity_type=competitions", "competitions"),
        ]

        for base_url, category in api_base_urls:
            for page in range(1, MAX_PAGES + 1):
                try:
                    url = f"{base_url}&page={page}&per_page={PER_PAGE}"
                    data = self.fetch_json(url)
                    if not data:
                        break

                    items = data if isinstance(data, list) else data.get("data", [])
                    if not items:
                        break

                    new_count = 0
                    for item in items:
                        title = item.get("name", "") or item.get("title", "")
                        description = item.get("description", "") or item.get("short_description", "")
                        href = item.get("url", "") or item.get("seo_url", "")

                        if not title or title in seen:
                            continue
                        seen.add(title)
                        new_count += 1

                        problems.append(ScrapedProblem(
                            title=title,
                            description=description or f"Competition on Unstop platform.",
                            source_platform=self.platform_name,
                            source_link=href if href.startswith("http") else f"https://unstop.com{href}",
                            domain=classify_domain(title, description),
                            tags=extract_tags(title, description),
                            difficulty=classify_difficulty(title, description),
                        ))

                    if new_count == 0:
                        break

                    if len(items) < PER_PAGE:
                        break

                    time.sleep(0.5)
                except Exception as e:
                    logger.warning(f"Unstop API page {page} failed: {e}")
                    break

        logger.info(f"Unstop: Extracted {len(problems)} opportunities")
        return problems
