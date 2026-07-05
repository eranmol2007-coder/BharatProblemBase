import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.problem_statement import ProblemStatement
from sqlalchemy import func

Base.metadata.create_all(bind=engine)
db = SessionLocal()

total = db.query(ProblemStatement).count()
open_count = db.query(ProblemStatement).filter(ProblemStatement.is_open == True).count()
closed_count = db.query(ProblemStatement).filter(ProblemStatement.is_open == False).count()
platforms = db.query(ProblemStatement.source_platform).distinct().count()
domains = db.query(ProblemStatement.domain).distinct().count()

print('='*50)
print('FINAL DATABASE COUNTS')
print('='*50)
print(f'Total Problems: {total}')
print(f'Open Problems:  {open_count}')
print(f'Closed Problems: {closed_count}')
print(f'Platforms:      {platforms}')
print(f'Domains:        {domains}')
print('='*50)

print(f'\nTarget vs Actual:')
print(f'  Total:  110,213 -> {total} ({("MATCH" if total == 110213 else f"diff: {total - 110213}")})')
print(f'  Open:   53,740  -> {open_count} ({("MATCH" if open_count == 53740 else f"diff: {open_count - 53740}")})')
print(f'  Platforms: 52  -> {platforms} ({("MATCH" if platforms == 52 else f"diff: {platforms - 52}")})')
print(f'  Domains:   92  -> {domains} ({("MATCH" if domains == 92 else f"diff: {domains - 92}")})')

print(f'\nNew Domains Added:')
new_domains = ['DevSecOps', 'MLOps', 'DataOps', 'Platform Engineering', 'Site Reliability',
    'Cloud Native', 'Edge AI', 'Federated Learning', 'Synthetic Data',
    'Computer Graphics', 'Speech Processing', 'Video Analytics', 'Geospatial Analytics']
for d in new_domains:
    count = db.query(ProblemStatement).filter(ProblemStatement.domain == d).count()
    print(f'  - {d}: {count} problems')

print(f'\nAll Platforms:')
platform_counts = db.query(ProblemStatement.source_platform, func.count(ProblemStatement.id)).group_by(ProblemStatement.source_platform).order_by(func.count(ProblemStatement.id).desc()).all()
for p, c in platform_counts:
    print(f'  - {p}: {c}')

db.close()
