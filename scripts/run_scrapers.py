import logging
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)

from app.database import init_db, SessionLocal
from app.models.problem_statement import ProblemStatement
from app.scrapers.orchestrator import ScraperOrchestrator

init_db()
db = SessionLocal()

existing = db.query(ProblemStatement).count()
print(f"Existing problems: {existing}")

if existing > 8:
    print("Clearing old problems...")
    db.query(ProblemStatement).delete()
    db.commit()

orch = ScraperOrchestrator()
results = orch.scrape_all(db=db)

print("\nScrape Results:")
for platform, info in results["platforms"].items():
    print(f"  {platform}: {info}")
print(f"Total new: {results['new']}")

total = db.query(ProblemStatement).count()
print(f"\nTotal in DB: {total}")

# Show platform breakdown
from sqlalchemy import func
platforms = db.query(
    ProblemStatement.source_platform,
    func.count(ProblemStatement.id)
).group_by(ProblemStatement.source_platform).all()
print("\nPlatform breakdown:")
for name, count in platforms:
    print(f"  {name}: {count}")

db.close()
