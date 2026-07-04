import json
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine, SessionLocal
from app.models import ProblemStatement

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SEED_FILE = os.path.join(DATA_DIR, "seed_problems.json")
SIH_FILE = os.path.join(DATA_DIR, "sih_problems.json")
PLATFORM_FILE = os.path.join(DATA_DIR, "platform_problems.json")
MORE_PLATFORMS_FILE = os.path.join(DATA_DIR, "more_platforms.json")


def create_tables():
    Base.metadata.create_all(bind=engine)


def _load_json_file(filepath: str, db, label: str) -> tuple[int, int]:
    if not os.path.isfile(filepath):
        return 0, 0

    with open(filepath, "r", encoding="utf-8") as f:
        problems = json.load(f)

    inserted = 0
    skipped = 0

    for item in problems:
        exists = (
            db.query(ProblemStatement)
            .filter(ProblemStatement.title == item["title"])
            .first()
        )
        if exists:
            skipped += 1
            continue

        db.add(ProblemStatement(**item))
        inserted += 1

    print(f"{label}: Inserted {inserted}, Skipped {skipped}")
    return inserted, skipped


def load_seed_data():
    db = SessionLocal()
    try:
        total_inserted = 0
        total_skipped = 0

        for filepath, label in [(SEED_FILE, "Seed"), (SIH_FILE, "SIH"), (PLATFORM_FILE, "Platform"), (MORE_PLATFORMS_FILE, "More")]:
            ins, skp = _load_json_file(filepath, db, label)
            total_inserted += ins
            total_skipped += skp

        db.commit()
        print(f"Total: Inserted {total_inserted}, Skipped {total_skipped}")
        return total_inserted

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


def ensure_seed_data(min_count: int = 10) -> int:
    """Load seed + SIH data if the database has fewer than min_count problems."""
    create_tables()
    db = SessionLocal()
    try:
        count = db.query(ProblemStatement).count()
        if count >= min_count:
            return 0
        logger.info(f"Database has {count} problems, loading seed data...")
    finally:
        db.close()

    return load_seed_data()


if __name__ == "__main__":
    print("Creating tables...")
    create_tables()
    print("Tables ready.")
    load_seed_data()
