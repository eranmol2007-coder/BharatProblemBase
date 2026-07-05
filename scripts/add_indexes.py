"""Add indexes to speed up search queries on the problems table."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bharatproblembase.db")

def add_indexes():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    indexes = [
        ("idx_title", "problem_statements(title)"),
        ("idx_domain", "problem_statements(domain)"),
        ("idx_platform", "problem_statements(source_platform)"),
        ("idx_difficulty", "problem_statements(difficulty)"),
        ("idx_organization", "problem_statements(organization)"),
        ("idx_category", "problem_statements(category)"),
        ("idx_is_open", "problem_statements(is_open)"),
        ("idx_source_year", "problem_statements(source_year)"),
        ("idx_created_at", "problem_statements(created_at)"),
    ]

    for name, def_ in indexes:
        try:
            cur.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {def_}")
            print(f"  Index {name} ready")
        except Exception as e:
            print(f"  Index {name} already exists or error: {e}")

    conn.commit()
    conn.close()
    print("All indexes applied.")

if __name__ == "__main__":
    add_indexes()
