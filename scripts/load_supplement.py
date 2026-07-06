import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.problem_statement import ProblemStatement

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SUPPLEMENT_FILES = [
    os.path.join(DATA_DIR, "supplement_problems.json"),
    os.path.join(DATA_DIR, "supplement2_problems.json"),
]

def load_supplement():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        total_inserted = 0
        total_skipped = 0

        for sup_file in SUPPLEMENT_FILES:
            if not os.path.exists(sup_file):
                print(f"Skipping {sup_file} - file not found")
                continue

            with open(sup_file, "r", encoding="utf-8") as f:
                problems = json.load(f)

            print(f"\nLoading {len(problems)} problems from {os.path.basename(sup_file)}")

            inserted = 0
            skipped = 0

            for i, item in enumerate(problems):
                exists = db.query(ProblemStatement).filter(ProblemStatement.title == item["title"], ProblemStatement.source_platform == item.get("source_platform", "general")).first()
                if exists:
                    skipped += 1
                    continue

                problem = ProblemStatement(
                    title=item["title"],
                    description=item["description"],
                    domain=item.get("domain"),
                    organization=item.get("organization"),
                    category=item.get("category"),
                    source_platform=item.get("source_platform"),
                    source_year=item.get("source_year"),
                    source_link=item.get("source_link"),
                    tags=item.get("tags"),
                    difficulty=item.get("difficulty"),
                    is_open=item.get("is_open", True),
                )
                db.add(problem)
                inserted += 1

                if (i + 1) % 5000 == 0:
                    db.commit()

            db.commit()
            total_inserted += inserted
            total_skipped += skipped
            print(f"  Inserted: {inserted}, Skipped: {skipped}")

        print(f"\nTotal Inserted: {total_inserted}, Total Skipped: {total_skipped}")

        # Print final counts
        total = db.query(ProblemStatement).count()
        open_count = db.query(ProblemStatement).filter(ProblemStatement.is_open == True).count()
        platforms = db.query(ProblemStatement.source_platform).distinct().count()
        domains = db.query(ProblemStatement.domain).distinct().count()

        print(f"\nFinal Database Counts:")
        print(f"  Total Problems: {total}")
        print(f"  Open Problems: {open_count}")
        print(f"  Platforms: {platforms}")
        print(f"  Domains: {domains}")

    finally:
        db.close()

if __name__ == "__main__":
    load_supplement()
