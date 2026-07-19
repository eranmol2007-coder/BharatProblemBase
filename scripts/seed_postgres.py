"""
Seed PostgreSQL database from local SQLite database or JSON files.
Usage: python scripts/seed_postgres.py <DATABASE_URL>

Example:
  python scripts/seed_postgres.py "postgresql://user:pass@host/dbname"
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import ProblemStatement

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

JSON_FILES = [
    ("seed_problems.json", "Seed"),
    ("sih_problems.json", "SIH"),
    ("platform_problems.json", "Platform"),
    ("more_platforms.json", "More"),
    ("curated_problems.json", "Curated"),
    ("supplement_problems.json", "Supplement"),
    ("supplement2_problems.json", "Supplement2"),
]


def seed_from_json(database_url: str):
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = Session()
    try:
        existing = db.query(ProblemStatement).count()
        if existing > 0:
            print(f"Database already has {existing} problems. Skipping seed.")
            return

        total_inserted = 0
        for filename, label in JSON_FILES:
            filepath = os.path.join(DATA_DIR, filename)
            if not os.path.isfile(filepath):
                print(f"  {label}: File not found, skipping")
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                problems = json.load(f)

            if not problems:
                print(f"  {label}: Empty, skipping")
                continue

            inserted = 0
            for item in problems:
                exists = (
                    db.query(ProblemStatement)
                    .filter(
                        ProblemStatement.title == item["title"],
                        ProblemStatement.source_platform == item.get("source_platform", "general"),
                    )
                    .first()
                )
                if exists:
                    continue
                db.add(ProblemStatement(**item))
                inserted += 1

            db.commit()
            total_inserted += inserted
            print(f"  {label}: Inserted {inserted}")

        print(f"\nTotal inserted: {total_inserted}")
    finally:
        db.close()


def seed_from_sqlite(sqlite_path: str, database_url: str):
    import sqlite3

    pg_engine = create_engine(database_url)
    PgSession = sessionmaker(bind=pg_engine)

    print("Creating PostgreSQL tables...")
    Base.metadata.create_all(bind=pg_engine)

    pg_db = PgSession()
    try:
        existing = pg_db.query(ProblemStatement).count()
        if existing > 0:
            print(f"PostgreSQL already has {existing} problems. Skipping.")
            return
    finally:
        pg_db.close()

    print(f"Reading from SQLite: {sqlite_path}")
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT * FROM problem_statements")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} problems in SQLite")

    columns = [desc[0] for desc in cursor.description]
    pg_db = PgSession()
    try:
        inserted = 0
        for row in rows:
            data = dict(zip(columns, row))
            data.pop("id", None)
            pg_db.add(ProblemStatement(**data))
            inserted += 1
            if inserted % 10000 == 0:
                pg_db.commit()
                print(f"  Inserted {inserted}/{len(rows)}...")

        pg_db.commit()
        print(f"Total inserted: {inserted}")
    except Exception as e:
        pg_db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        pg_db.close()
        sqlite_conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python seed_postgres.py <DATABASE_URL>")
        print('Example: python seed_postgres.py "postgresql://user:pass@host/dbname"')
        sys.exit(1)

    database_url = sys.argv[1]
    print(f"Target: {database_url}")

    sqlite_path = os.path.join(DATA_DIR, "bharatproblembase.db")
    if os.path.isfile(sqlite_path):
        print("\nSeeding from SQLite database...")
        seed_from_sqlite(sqlite_path, database_url)
    else:
        print("\nSeeding from JSON files...")
        seed_from_json(database_url)

    print("\nDone! Set this DATABASE_URL in your Vercel project settings.")
