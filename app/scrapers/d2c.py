import logging
import time

from app.scrapers.base import BaseScraper, ScrapedProblem
from app.ml.classifier import classify_domain, extract_tags, classify_difficulty

logger = logging.getLogger(__name__)

MAX_PAGES = 50
PAGE_SIZE = 100


class D2CScraper(BaseScraper):
    platform_name = "D2C"

    def scrape(self) -> list[ScrapedProblem]:
        problems = []

        problems.extend(self._scrape_with_cookies())
        problems.extend(self._scrape_via_api())

        return problems

    def _scrape_with_cookies(self) -> list[ScrapedProblem]:
        problems = []
        url = "https://dare2compete.com/hackathons"

        self.session.cookies.set("cookie_consent", "true", domain="dare2compete.com")
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })

        soup = self.fetch_page(url)
        if not soup:
            return problems

        if "Cookies Disabled" in soup.get_text():
            logger.warning("D2C: Cookies required, trying API")
            return self._scrape_via_api()

        cards = soup.select("[class*=card], [class*=hackathon], [class*=opportunity], [class*=listing]")
        logger.info(f"D2C: Found {len(cards)} potential cards")

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
                    href = f"https://dare2compete.com{href}"

                org_el = card.select_one(".organization, .org, .company, .organizer")
                organization = org_el.get_text(strip=True) if org_el else None

                if not description:
                    description = f"Hackathon on D2C platform."

                problems.append(ScrapedProblem(
                    title=title,
                    description=description,
                    source_platform=self.platform_name,
                    source_link=href or url,
                    organization=organization,
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
            "https://dare2compete.com/api/public/opportunity/search?type=hackathons",
            "https://dare2compete.com/api/public/opportunity/search?type=competitions",
        ]

        for base_url in api_base_urls:
            for page in range(1, MAX_PAGES + 1):
                try:
                    url = f"{base_url}&page={page}&size={PAGE_SIZE}"
                    data = self.fetch_json(url)
                    if not data:
                        break

                    items = data if isinstance(data, list) else data.get("data", []) or data.get("results", [])
                    if not items:
                        break

                    new_count = 0
                    for item in items:
                        title = item.get("name", "") or item.get("title", "")
                        description = item.get("description", "") or item.get("short_desc", "")
                        href = item.get("url", "") or item.get("slug", "")
                        organization = item.get("organization", "") or item.get("organizer", "")

                        if not title or title in seen:
                            continue
                        seen.add(title)
                        new_count += 1

                        problems.append(ScrapedProblem(
                            title=title,
                            description=description or f"Competition on D2C platform.",
                            source_platform=self.platform_name,
                            source_link=href if href.startswith("http") else f"https://dare2compete.com/{href}",
                            organization=organization,
                            domain=classify_domain(title, description),
                            tags=extract_tags(title, description),
                            difficulty=classify_difficulty(title, description),
                        ))

                    if new_count == 0:
                        break

                    if len(items) < PAGE_SIZE:
                        break

                    time.sleep(0.5)
                except Exception as e:
                    logger.warning(f"D2C API page {page} failed: {e}")
                    break

        logger.info(f"D2C: Extracted {len(problems)} opportunities")
        return problems
