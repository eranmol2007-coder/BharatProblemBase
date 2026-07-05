import logging
import os
from typing import Optional

from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, ScrapedProblem

logger = logging.getLogger(__name__)


class SIHScraper(BaseScraper):
    platform_name = "Smart India Hackathon"

    def scrape(self) -> list[ScrapedProblem]:
        problems = []

        problems.extend(self._scrape_2025_html())
        problems.extend(self._scrape_2024_excel())

        return problems

    def _scrape_2025_html(self) -> list[ScrapedProblem]:
        problems = []
        url = "https://www.sih.gov.in/sih2025PS"
        soup = self.fetch_page(url)
        if not soup:
            return problems

        tables = soup.find_all("table")
        logger.info(f"SIH 2025: Found {len(tables)} tables")

        if not tables:
            return problems

        for table in tables:
            has_ps_id = table.find("th", string=lambda s: s and "Problem Statement ID" in s.strip())
            if not has_ps_id:
                continue

            rows = table.find_all("tr")
            ps_data = {}
            for row in rows:
                cells = row.find_all(["th", "td"])
                if len(cells) < 2:
                    continue

                th = cells[0].get_text(strip=True)
                td = cells[1].get_text(strip=True) if len(cells) > 1 else ""

                if "Problem Statement ID" in th:
                    ps_data = {"id": td}
                elif "Problem Statement Title" in th:
                    ps_data["title"] = td
                elif "Description" in th:
                    ps_data["description"] = td
                elif "Organization" in th:
                    ps_data["organization"] = td
                elif "Department" in th:
                    ps_data["department"] = td
                elif "Category" in th:
                    ps_data["category"] = td
                elif "Theme" in th:
                    ps_data["theme"] = td

            if ps_data.get("id") and ps_data.get("title"):
                problem = self._make_problem(ps_data, url)
                if problem:
                    problems.append(problem)

        logger.info(f"SIH 2025: Extracted {len(problems)} problems")
        return problems

    def _make_problem(self, data: dict, base_url: str) -> Optional[ScrapedProblem]:
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        if not title or not description:
            return None

        if description.startswith("Problem Statement"):
            description = description[len("Problem Statement"):].strip()

        description = self._clean_description(description)
        title = self._clean_title(title)

        return ScrapedProblem(
            title=title,
            description=description,
            source_platform=self.platform_name,
            source_link=f"{base_url}#{data.get('id', '')}",
            source_year=2025,
            organization=data.get("organization") or data.get("department"),
            category=data.get("category"),
            domain=data.get("theme", ""),
        )

    def _scrape_2024_excel(self) -> list[ScrapedProblem]:
        problems = []
        excel_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data", "SIH_PS_2024.xlsx"
        )

        if not os.path.isfile(excel_path):
            logger.info("SIH 2024 Excel not found locally, downloading...")
            self._download_excel(excel_path)

        if not os.path.isfile(excel_path):
            logger.warning("SIH 2024 Excel not available")
            return problems

        try:
            import openpyxl
            wb = openpyxl.load_workbook(excel_path)
            sheet = wb.active

            headers = [cell.value for cell in sheet[1]]
            title_idx = headers.index("Title") if "Title" in headers else -1
            desc_idx = headers.index("Description") if "Description" in headers else -1
            cat_idx = headers.index("Category") if "Category" in headers else -1
            org_idx = headers.index("Organisation") if "Organisation" in headers else -1
            dept_idx = headers.index("Department") if "Department" in headers else -1
            domain_idx = headers.index("Technology_Bucket") if "Technology_Bucket" in headers else -1
            ps_id_idx = headers.index("Statement_id") if "Statement_id" in headers else -1

            for row in sheet.iter_rows(min_row=2, values_only=True):
                title = str(row[title_idx]).strip() if title_idx >= 0 and row[title_idx] else ""
                description = str(row[desc_idx]).strip() if desc_idx >= 0 and row[desc_idx] else ""

                if not title or not description:
                    continue

                description = self._clean_description(description)
                title = self._clean_title(title)
                ps_id = str(row[ps_id_idx]).strip() if ps_id_idx >= 0 and row[ps_id_idx] else ""

                problems.append(ScrapedProblem(
                    title=title,
                    description=description,
                    source_platform=self.platform_name,
                    source_link=f"https://www.sih.gov.in/sih2024",
                    source_year=2024,
                    organization=str(row[org_idx]).strip() if org_idx >= 0 and row[org_idx] else None,
                    category=str(row[cat_idx]).strip() if cat_idx >= 0 and row[cat_idx] else None,
                    domain=str(row[domain_idx]).strip() if domain_idx >= 0 and row[domain_idx] else None,
                ))

            logger.info(f"SIH 2024: Extracted {len(problems)} problems from Excel")

        except Exception as e:
            logger.error(f"Error parsing SIH 2024 Excel: {e}")

        return problems

    def _download_excel(self, path: str):
        url = "https://www.sih.gov.in/letters/SIH_PS_2024.xlsx"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    f.write(r.content)
                logger.info(f"Downloaded SIH 2024 Excel ({len(r.content)} bytes)")
        except Exception as e:
            logger.error(f"Failed to download SIH 2024 Excel: {e}")

    def _clean_description(self, desc: str) -> str:
        desc = desc.replace("Problem Statement", "", 1).strip()
        desc = desc.replace("Description", "", 1).strip()
        desc = desc.replace("\u00a0", " ").strip()
        while "  " in desc:
            desc = desc.replace("  ", " ")
        return desc[:5000]

    def _clean_title(self, title: str) -> str:
        title = title.replace("\u00a0", " ").strip()
        while "  " in title:
            title = title.replace("  ", " ")
        return title[:500]
