"""Load SIH problem statements from data/sih_problems.json into the database."""
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine, SessionLocal
from app.models import ProblemStatement

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SIH_FILE = os.path.join(DATA_DIR, "sih_problems.json")


def load_sih_data():
    if not os.path.isfile(SIH_FILE):
        print(f"SIH data file not found: {SIH_FILE}")
        return 0

    Base.metadata.create_all(bind=engine)

    with open(SIH_FILE, "r", encoding="utf-8") as f:
        problems = json.load(f)

    db = SessionLocal()
    inserted = 0
    skipped = 0

    try:
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

        db.commit()
        print(f"SIH load complete. Inserted: {inserted}, Skipped: {skipped}")
        return inserted

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_sih_data()
